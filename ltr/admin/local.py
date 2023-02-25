class EnvironmentSettings:
    def __init__(self):
        self.workspace_dir = '/home/wcz/Yang/DPET/ltr/checkpoints/'    # Base directory for saving network checkpoints.
        self.tensorboard_dir = self.workspace_dir + '/tensorboard/'    # Directory for tensorboard files.
        self.lasot_dir = '/media/wcz/disk2/transtrack/TransT_train/dataset/LaSOT/LaSOTBenchmark'
        self.got10k_dir = '/media/wcz/disk2/transtrack/TransT_train/dataset/Got10k/train'
        self.trackingnet_dir = ''
        self.coco_dir = ''
        self.imagenet_dir = ''
        self.imagenetdet_dir = ''
        self.pregenerated_masks = '/media/wcz/disk2/transtrack/TransT_train/dataset/pre_masks/'
        self.davis_dir = '/media/wcz/disk2/transtrack/TransT_train/dataset/DAVIS/'
        self.vos_dir = '/home/wcz/Yang/JCAT_train/ltr/dataset/YouTube_VOS/train/'
