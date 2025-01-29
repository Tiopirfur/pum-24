import streamlit as st
import pandas as pd
import pickle as pkl
from rdkit import Chem
from rdkit.Chem import rdMolDescriptors
from rdkit.Chem import Crippen
from sklearn.preprocessing import StandardScaler

class Featurizer:
    def __init__(self, smiles):
        #self.smiles = smiles
        self.scaler = StandardScaler()
        train_des = self.get_des(smiles)
        self.scaler.fit(train_des)
    
    def featurize(self, smiles):
        des = self.get_des(smiles)
        scaled_des = self.scaler.transform(des)
        return scaled_des

    def get_des(self, smiles):
        df = pd.DataFrame({'SMILES':smiles})
        df['mol'] = df['SMILES'].apply(Chem.MolFromSmiles)
        df['mol_wt'] = df['mol'].apply(rdMolDescriptors.CalcExactMolWt)             # Molecular weight
        df['logp'] = df['mol'].apply(Crippen.MolLogP)                               # LogP (lipophilicity)
        df['num_heavy_atoms'] = df['mol'].apply(rdMolDescriptors.CalcNumHeavyAtoms) # Number of heavy atoms
        df['num_HBD'] = df['mol'].apply(rdMolDescriptors.CalcNumHBD)                # Number of hydrogen bond donors
        df['num_HBA'] = df['mol'].apply(rdMolDescriptors.CalcNumHBA)                # Number of hydrogen bond acceptors
        df['aromatic_rings'] = df['mol'].apply(rdMolDescriptors.CalcNumAromaticRings) # Number of aromatic rings
        return df[['mol_wt','logp','num_heavy_atoms','num_HBD','num_HBA','aromatic_rings']]

with open('data/svr.pkl', 'rb') as f:
    svr = pkl.load(f)
with open('data/featurizer.pkl', 'rb') as f:
    featurizer = pkl.load(f)
    
st.title('Solvatation Predictor')

st.write('Solvatation Predictor is a tool for prediction of solubility based on SMILES code')

smileses = st.text_area('Insert 1 or multiple SMILES codes (remember 1 SMILES in 1 row!', '')

if st.button('Calculate.'):
    if not smileses:
        st.stop()
    with st.empty():
        #SMILES = pd.Series(smileses.split())
        X = featurizer.featurize(smileses.split())
        y_pred = svr.predict(X)
        st.write(pd.DataFrame({'SMILES':smileses.split(), 'Solubility':y_pred}))