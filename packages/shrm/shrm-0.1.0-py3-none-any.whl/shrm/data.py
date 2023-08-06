import os
import torch
from scipy.io import loadmat
import tarfile


class CWRUDataset:
    PATH = os.path.dirname(os.path.abspath(__file__))
    DATASET_PATH = os.path.join(PATH, 'data')
    LOADS = [0, 1, 2, 3]
    LABELS = ['N_0', 'I_7', 'I_14', 'I_21', 'B_7', 'B_14', 'B_21', 'O_7', 'O_14', 'O_21']
    SAMPLING_RATE = 12000
    MAX_LENGTH = 121265

    def __init__(self, loads=LOADS, labels=LABELS,
                 split_constant_length=MAX_LENGTH):
        self.__labels = labels
        self.__loads = loads
        self.__length = split_constant_length
        self.label_to_int = dict(sorted(zip(self.labels, range(len(self.labels)))))
        self.int_to_label = {ints: label for label, ints in zip(self.label_to_int.keys(), self.label_to_int.values())}
        self.X, self.y = self._get_dataset_from_data_path()

    @property
    def loads(self):
        return self.__loads

    @loads.setter
    def loads(self, values):
        for value in values:
            if not value in CWRUDataset.LOADS:
                raise Exception(f'Not Exist Load Value. There is onl {CWRUDataset.LOADS}')

        return values

    @property
    def labels(self):
        return self.__labels

    @labels.setter
    def labels(self, values):
        for value in values:
            if not value in CWRUDataset.LABELS:
                raise Exception(f'Not Exist Load LABELS. There is only {CWRUDataset.LABELS}')

        return values

    @property
    def length(self):
        return self.__length

    @length.setter
    def length(self, value):
        if value > CWRUDataset.MAX_LENGTH:
            raise Exception(f' Should be smaller than {CWRUDataset.MAX_LENGTH}')

        return value

    def __getitem__(self, index):
        return self.X[index], self.y[index]

    def __len__(self):
        return len(self.X)

    def _get_dataset_from_data_path(self):
        X = []
        y = []
        LABEL_PATH = [i for i in os.listdir(CWRUDataset.DATASET_PATH) if i in CWRUDataset.LABELS]

        # shrm_dir = os.path.join(os.path.expanduser("~"), '.shrm')
        # os.makedirs(shrm_dir, exist_ok=True)
        # shrm_file = os.path.join(shrm_dir,'cwru.tar.gz')
        #
        #
        # file_id = 'https://drive.google.com/file/d/105IThQbioVIvVpH45udX4wHKXeixHbyn/view?usp=sharing'
        # download_file_from_google_drive(file_id, shrm_file)
        #
        # tar = tarfile.open(os.path.join(CWRUDataset.DATASET_PATH, 'cwru.tar.gz'))
        # tar.extractall(CWRUDataset.DATASET_PATH)
        # tar.close()

        for label in LABEL_PATH:
            for load, load_file_name in enumerate(sorted(
                    [j for j in os.listdir(os.path.join(CWRUDataset.DATASET_PATH, label)) if
                     (j.endswith('.mat') == True and j.startswith('.') == False)])):
                if load in self.loads:
                    KEY = 'X' + load_file_name.split('.')[0] + '_DE_time'  # (TODO) DE_time으로 하는게 맞는지
                    signal_channel = loadmat(os.path.join(CWRUDataset.DATASET_PATH, label, load_file_name))[
                        KEY].T  # shape (1, length)
                    X.append(signal_channel[:, :self.length])
                    y.append(self.label_to_int[label])

        X = torch.Tensor(X)
        y = torch.Tensor(y)

        return X, y
