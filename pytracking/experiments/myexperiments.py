from pytracking.evaluation import Tracker, OTBDataset, VOTDataset, TrackingNetDataset, GOT10KDatasetTest, VOT16Dataset, VOT18Dataset, VOT19Dataset, NFSDataset, UAVDataset, TPLDataset, LaSOTDataset

########## Coding by Yang 2021.11 ######## run experiments on benchmarks #####################################
def got10k():
    # Run experiment on the Got10k dataset
    trackers = [Tracker('dpet', 'dpet')]

    dataset = GOT10KDatasetTest()
    return trackers, dataset      

def trackingnet():
    # Run experiment on the TrackingNet dataset
    trackers = [Tracker('dpet', 'dpet')]

    dataset = TrackingNetDataset()
    return trackers, dataset    

def otb():
    # Run experiment on the OTB100 dataset
    trackers = [Tracker('dpet', 'dpet')]

    dataset = OTBDataset()
    return trackers, dataset

def nfs():
    # Run experiment on the NFS dataset
    trackers = [Tracker('dpet', 'dpet')]

    dataset = NFSDataset()
    return trackers, dataset    

def tcl128():
    # Run experiment on the TCL128 dataset
    trackers = [Tracker('dpet', 'dpet')]

    dataset = TPLDataset()
    return trackers, dataset   

def lasot():
    # Run experiment on the LaSOT dataset
    trackers = [Tracker('dpet', 'dpet')]

    dataset = LaSOTDataset()
    return trackers, dataset 

def uav123():
    # Run experiment on the UAV123 dataset
    trackers = [Tracker('dpet', 'dpet')]

    dataset = UAVDataset()
    return trackers, dataset
