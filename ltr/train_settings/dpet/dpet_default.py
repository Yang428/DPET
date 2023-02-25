import os
import torch
import torch.nn as nn
import torch.optim as optim
import torchvision.transforms

from ltr.dataset import Vos, Got10kVOS, LasotVOS, Davis
from ltr.data import dpet_processing, dpet_sampler, LTRLoader
import ltr.models.dpet.dpet as segm_models
from ltr import actors
from ltr.trainers import LTRTrainer
import ltr.data.transforms as dltransforms

## modify loss function ##
class ModifyLoss(torch.nn.Module):
    def __init__(self):
        super().__init__()

    def forward(self, mask_pred, mask_contour, mask):#, scores):
        belta = 1             # emphasize factor of edges 
        mask_pred = 1/(1+torch.exp(-mask_pred/2)) # sigmoid function, /2 enlarge the gap
        if mask_contour is None:
            loss = mask*torch.log(mask_pred+1e-10) + (1-mask)*torch.log(1-mask_pred+1e-10)
            return torch.mean(-loss)
        #scores = 1/(1+torch.exp(-scores/2))
        #cmask = nn.functional.interpolate(mask[:,:1,:,:], size=(24, 24))
        # foreground loss and background loss
        loss1 = (mask[:,0,:,:] + belta*mask_contour[:,0,:,:])*torch.log(mask_pred[:,0,:,:]+1e-10) + (1-mask[:,0,:,:])*torch.log(1-mask_pred[:,0,:,:]+1e-10)
        loss2 = mask[:,1,:,:]*torch.log(mask_pred[:,1,:,:]+1e-10) + (1-mask[:,1,:,:])*torch.log(1-mask_pred[:,1,:,:]+1e-10) # 1e-10, avoid zero element in log function
        #loss3 = cmask*torch.log(scores+1e-10) + (1-cmask)*torch.log(1-scores+1e-10)
        loss = torch.mean(-(loss1+loss2))
        return loss

def run(settings):
    # Most common settings are assigned in the settings struct
    settings.description = 'SegmentationNet with default settings.'
    settings.print_interval = 1  # How often to print loss and other info  
    settings.batch_size = 32  # Batch size
    settings.num_workers = 8  # Number of workers for image loading
    settings.normalize_mean = [0.485, 0.456, 0.406]  # Normalize mean (default pytorch ImageNet values)
    settings.normalize_std = [0.229, 0.224, 0.225]  # Normalize std (default pytorch ImageNet values)
    settings.search_area_factor = 4.0  # Image patch size relative to target size
    settings.feature_sz = 24  # Size of feature map
    settings.output_sz = settings.feature_sz * 16  # Size of input image patches

    # Settings for the image sample and proposal generation
    settings.center_jitter_factor = {'train': 0, 'test': 1.5}
    settings.scale_jitter_factor = {'train': 0, 'test': 0.25}

    settings.segm_topk_pos = 3
    settings.segm_topk_neg = 3

    settings.segm_use_distance = True

    mixer_channels = 3

    # check if debug folder exists
    if not os.path.isdir(settings.env.workspace_dir):
        os.mkdir(settings.env.workspace_dir)

    settings.env.images_dir = os.path.join(settings.env.workspace_dir, 'images')
    if not os.path.isdir(settings.env.images_dir):
        os.mkdir(settings.env.images_dir)

    # Train datasets
    anno_path = os.path.join(settings.env.pregenerated_masks, "got10k_masks")
    got10k_train = Got10kVOS(anno_path=anno_path, split='vottrain')

    lasot_anno_path = os.path.join(settings.env.pregenerated_masks, "lasot_masks")
    lasot_train = LasotVOS(anno_path=lasot_anno_path, split='train')

    #davis_train = Davis(version='2017', multiobj=False, split='train')

    vos_train = Vos(split='train')

    # Validation datasets
    vos_val = Vos(split='val')

    # The joint augmentation transform, that is applied to the pairs jointly
    # No need for grayscale transformation since we are doing color segmentation
    # transform_joint = dltransforms.ToGrayscale(probability=0.05)

    # The augmentation transform applied to the training set (individually to each image in the pair)
    transform_train = torchvision.transforms.Compose([dltransforms.ToTensorAndJitter(0.2),
                                                      torchvision.transforms.Normalize(mean=settings.normalize_mean,
                                                                                       std=settings.normalize_std)])

    # The augmentation transform applied to the validation set (individually to each image in the pair)
    transform_val = torchvision.transforms.Compose([torchvision.transforms.ToTensor(),
                                                    torchvision.transforms.Normalize(mean=settings.normalize_mean,
                                                                                     std=settings.normalize_std)])

    # Data processing to do on the training pairs
    data_processing_train = dpet_processing.DPETProcessing(search_area_factor=settings.search_area_factor,
                                                               output_sz=settings.output_sz,
                                                               center_jitter_factor=settings.center_jitter_factor,
                                                               scale_jitter_factor=settings.scale_jitter_factor,
                                                               mode='pair',
                                                               transform=transform_train,
                                                               use_distance=settings.segm_use_distance)

    # Data processing to do on the validation pairs
    data_processing_val = dpet_processing.DPETProcessing(search_area_factor=settings.search_area_factor,
                                                             output_sz=settings.output_sz,
                                                             center_jitter_factor=settings.center_jitter_factor,
                                                             scale_jitter_factor=settings.scale_jitter_factor,
                                                             mode='pair',
                                                             transform=transform_val,
                                                             use_distance=settings.segm_use_distance)

    # The sampler for training [vos_train, davis_train, got10k_train, lasot_train], [11, 1, 10, 10],
    dataset_train = dpet_sampler.DPETSampler([vos_train,got10k_train,lasot_train], [1,1,1],
                                             samples_per_epoch=1500 * settings.batch_size, max_gap=50,
                                             processing=data_processing_train)

    # The loader for training
    loader_train = LTRLoader('train', dataset_train, training=True, batch_size=settings.batch_size,
                             num_workers=settings.num_workers,
                             shuffle=True, drop_last=True, stack_dim=1)

    # # The sampler for validation
    dataset_val = dpet_sampler.DPETSampler([vos_val], [1], samples_per_epoch=10 * settings.batch_size, max_gap=50,
                                           processing=data_processing_val)

    # # The loader for validation
    loader_val = LTRLoader('val', dataset_val, training=False, batch_size=settings.batch_size,
                           num_workers=settings.num_workers,
                           shuffle=False, drop_last=True, epoch_interval=1, stack_dim=1)

    # Create network
    # resnet50 or resnet18
    net = segm_models.dpet_resnet50(backbone_pretrained=True, topk_pos=settings.segm_topk_pos,
                                    topk_neg=settings.segm_topk_neg, mixer_channels=mixer_channels)

    # Set objective
    #objective = nn.BCEWithLogitsLoss()
    objective = ModifyLoss()

    # Create actor, which wraps network and objective
    actor = actors.DPETActor(net=net, objective=objective)

    # Optimizer
    optimizer = optim.Adam(actor.net.segm_predictor.parameters(), lr=1e-3)

    # Learning rate scheduler
    lr_scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=20, gamma=0.2)

    # Create trainer
    trainer = LTRTrainer(actor, [loader_train, loader_val], optimizer, settings, lr_scheduler)

    # Run training (set fail_safe=False if you are debugging)
    trainer.train(60, load_latest=True, fail_safe=False)
