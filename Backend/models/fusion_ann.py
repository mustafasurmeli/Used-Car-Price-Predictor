import torch
import torch.nn as nn
import torch.nn.functional as F


class FusionANN(nn.Module):
    def __init__(self,
                 text_input_dim=768,
                 numeric_input_dim=4,
                 ekspertiz_input_dim=13,
                 cat_embedding_input_dim=12,
                 fusion_output_dim=576,
                 hidden_sizes=(512,384, 256, 192, 128, 64),
                 dropout_rates=(0.2, 0.2, 0.2, 0.2)):

        super(FusionANN, self).__init__()

        self.text_layer = nn.Sequential(
            nn.Linear(text_input_dim, 256),
            nn.BatchNorm1d(256),
            nn.ReLU(),
            nn.Dropout(dropout_rates[0])
        )

        self.numeric_layer = nn.Sequential(
            nn.Linear(numeric_input_dim, 128),
            nn.BatchNorm1d(128),
            nn.ReLU(),
            nn.Dropout(dropout_rates[1])
        )

        self.ekspertiz_layer = nn.Sequential(
            nn.Linear(ekspertiz_input_dim, 64),
            nn.BatchNorm1d(64),
            nn.ReLU(),
            nn.Dropout(dropout_rates[2])
        )

        self.cat_embedding_layer = nn.Sequential(
            nn.Linear(cat_embedding_input_dim, 128),
            nn.BatchNorm1d(128),
            nn.ReLU(),
            nn.Dropout(dropout_rates[3])
        )

        self.fusion_layer = nn.Sequential(
            nn.Linear(fusion_output_dim, hidden_sizes[0]),
            nn.BatchNorm1d(hidden_sizes[0]),
            nn.LeakyReLU(),
            nn.Dropout(0.2),
            nn.Linear(hidden_sizes[0], hidden_sizes[1]),
            nn.BatchNorm1d(hidden_sizes[1]),
            nn.LeakyReLU(),
            nn.Dropout(0.2),
            nn.Linear(hidden_sizes[1], hidden_sizes[2]),
            nn.BatchNorm1d(hidden_sizes[2]),
            nn.LeakyReLU(),
            nn.Dropout(0.2),
            nn.Linear(hidden_sizes[2], hidden_sizes[3]),
            nn.BatchNorm1d(hidden_sizes[3]),
            nn.LeakyReLU(),
            nn.Dropout(0.2),
            nn.Linear(hidden_sizes[3], hidden_sizes[4]),
            nn.BatchNorm1d(hidden_sizes[4]),
            nn.LeakyReLU(),
            nn.Dropout(0.2),
            nn.Linear(hidden_sizes[4], hidden_sizes[5]),
            nn.BatchNorm1d(hidden_sizes[5]),
            nn.LeakyReLU(),
            nn.Linear(hidden_sizes[5], 1)
        )

    def forward(self, text_vec, numeric_vec, ekspertiz_vec, cat_vec):
        t = self.text_layer(text_vec)
        n = self.numeric_layer(numeric_vec)
        e = self.ekspertiz_layer(ekspertiz_vec)
        c = self.cat_embedding_layer(cat_vec)

        fused = torch.cat([t, n, e, c], dim=1)
        out = self.fusion_layer(fused)
        return out