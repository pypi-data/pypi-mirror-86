from rdkit.Chem.rdmolfiles import MolFromSmarts, MolFromSmiles, MolToSmiles
from rdkit.Chem import AllChem
from rdkit.Chem import SaltRemover
from rdkit.Chem import rdmolops
from rdkit.Chem.rdmolops import RemoveHs


class FilterRegistry:

    def __init__(self):
        self._filters = {"neutralise_charges": self._neutralise_charges,
                         "get_largest_fragment": self._get_largest_fragment,
                         "remove_hydrogens": self._remove_hydrogens,
                         "remove_salts": self._remove_salts,
                         "general_cleanup": self._general_cleanup,
                         "rare_filters": self._rare_filters,
                         "valid_size": self._valid_size,
                         "default": self.standardize}

    def get_filter(self, filter_name: str):
        selected_filter=None
        try:
            selected_filter = self._filters.get(filter_name)
        except:
            KeyError(f'requested filter "{filter_name}" does not exist in the registry')
        return selected_filter

    def _get_largest_fragment(self, mol):
        frags = rdmolops.GetMolFrags(mol, asMols=True, sanitizeFrags=True)
        maxmol = None
        for mol in frags:
            if mol is None:
                continue
            if maxmol is None:
                maxmol = mol
            if maxmol.GetNumHeavyAtoms() < mol.GetNumHeavyAtoms():
                maxmol = mol
        return maxmol

    def _remove_hydrogens(self, mol):
        return RemoveHs(mol, implicitOnly=False, updateExplicitCount=False, sanitize=True)

    def _remove_salts(self, mol):
        return SaltRemover.SaltRemover().StripMol(mol, dontRemoveEverything=True)

    def _initialiseNeutralisationReactions(self):
        patts = (
            # Imidazoles
            ('[n+;H]', 'n'),
            # Amines
            ('[N+;!H0]', 'N'),
            # Carboxylic acids and alcohols
            ('[$([O-]);!$([O-][#7])]', 'O'),
            # Thiols
            ('[S-;X1]', 'S'),
            # Sulfonamides
            ('[$([N-;X2]S(=O)=O)]', 'N'),
            # Enamines
            ('[$([N-;X2][C,N]=C)]', 'N'),
            # Tetrazoles
            ('[n-]', '[nH]'),
            # Sulfoxides
            ('[$([S-]=O)]', 'S'),
            # Amides
            ('[$([N-]C=O)]', 'N'),
        )
        return [(MolFromSmarts(x), MolFromSmiles(y, False)) for x, y in patts]

    def _neutralise_charges(self, mol, reactions=None):
        if reactions is None:
            reactions = self._initialiseNeutralisationReactions()

        for i, (reactant, product) in enumerate(reactions):
            while mol.HasSubstructMatch(reactant):
                rms = AllChem.ReplaceSubstructs(mol, reactant, product)
                mol = rms[0]
        return mol

    def _general_cleanup(self, mol):
        rdmolops.Cleanup(mol)
        rdmolops.SanitizeMol(mol)
        mol = rdmolops.RemoveHs(mol, implicitOnly=False, updateExplicitCount=False, sanitize=True)
        return mol

    def _rare_filters(self, mol):
        if mol:
            cyano_filter = "[C-]#[N+]"
            oh_filter = "[OH+]"
            sulfur_filter = "[SH]"
            if not mol.HasSubstructMatch(MolFromSmarts(cyano_filter)) \
                    and not mol.HasSubstructMatch(MolFromSmarts(oh_filter)) \
                    and not mol.HasSubstructMatch(MolFromSmarts(sulfur_filter)):
                return mol

    def _valid_size(self, mol, min_heavy_atoms=2, max_heavy_atoms=70, element_list=None, remove_long_side_chains=True):
        """Filters molecules on number of heavy atoms and atom types"""
        if element_list is None:
            element_list = [6, 7, 8, 9, 16, 17, 35]

        if mol:
            correct_size = min_heavy_atoms < mol.GetNumHeavyAtoms() < max_heavy_atoms
            if not correct_size:
                return

            valid_elements = all([atom.GetAtomicNum() in element_list for atom in mol.GetAtoms()])
            if not valid_elements:
                return

            has_long_sidechains = False
            if remove_long_side_chains:
                # remove aliphatic side chains with at least 5 carbons not in a ring
                sma = '[CR0]-[CR0]-[CR0]-[CR0]-[CR0]'
                has_long_sidechains = mol.HasSubstructMatch(MolFromSmarts(sma))
            if correct_size and valid_elements and not has_long_sidechains:
                return mol

    def standardize(self, mol, min_heavy_atoms=2, max_heavy_atoms=70, element_list=None,
                           remove_long_side_chains=True, neutralise_charges=True):

        if mol:
            mol = self._get_largest_fragment(mol)
        if mol:
            mol = self._remove_hydrogens(mol)
        if mol:
            mol = self._remove_salts(mol)
        if mol and neutralise_charges:
            mol = self._neutralise_charges(mol)
        if mol:
            mol = self._general_cleanup(mol)
        if mol:
            mol = self._rare_filters(mol)
        if mol:
            mol = self._valid_size(mol, min_heavy_atoms, max_heavy_atoms, element_list, remove_long_side_chains)
            return mol
        return None
