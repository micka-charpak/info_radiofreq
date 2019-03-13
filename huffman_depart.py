class Arbre:
    def __init__(self, frequence, gauche, droit):
        """ Construit un Arbre

            frequence: int
            gauche, droit: Arbre
        """
        self.frequence = frequence
        self.gauche = gauche
        self.droit = droit

    def affiche(self, prefixes = ['    ']):
        """ Affiche l'arbre """
        print(''.join(prefixes[:-1]) + '|___' + str(self.frequence))
        prefixes.append('|   ')
        self.gauche.affiche(prefixes)
        prefixes.pop()
        prefixes.append('    ')
        self.droit.affiche(prefixes)
        prefixes.pop()

class Feuille(Arbre):
    def __init__(self, frequence, symbole):
        """ Construit une feuille

            frequence: int
            symbole: str
        """
        Arbre.__init__(self, frequence, None, None)
        self.symbole = symbole

    def affiche(self, prefixes = ['    ']):
        """ Affiche la feuille """
        print("".join(prefixes[:-1]) + '|___' +
                str(self.frequence) +
                '(' + self.symbole + ')')


def encode_ascii(texte):
    '''
    renvoie le codage ascii d'une chaîne de caractère
    :param texte: str
    :return: str de 0 et de 1 '10010100010110001...'
    >>> encode_ascii('bonjour')
    '01100010011011110110111001101010011011110111010101110010'
    '''
    texte_ascii=''
    for car in texte :
        texte_ascii += str(("{:08b}".format(ord(car))))
    return texte_ascii

def frequences(texte):
    '''
    renvoie un dictionnaire des caractères présents et de leur
    fréquence    :param texte:
    :return: dictionnaire de la forme {'A': 12, 'C': 3, ...}
    >>> frequences('ABRACADABRA')
    {'A': 5, 'B': 2, 'R': 2, 'C': 1, 'D': 1}
    '''
    l=[]
    d={}
    for i in range(len(texte)):
        if texte[i] not in texte[0:i] :
            d[texte[i]] = texte.count(texte[i])
    return d


class Huffman:
    """ Algorithme de construction de l'arbre de Huffman """
    def __init__(self, frequences):
        """ Constructeur

            frequences: dictionnaire des fréquences
        """
        self.foret = []
        for lettre in frequences.keys():
            self.foret.append(Feuille(frequences[lettre],lettre))
    def pop_min(self):
        """
        Retire la feuille avec la plus petite fréquence de la forêt et la retourne
        :return: Feuille
        >>> Huffman(frequences('ABRACADABRA')).pop_min().frequence == 1
        True
        """
        min = self.foret[0].frequence
        for i in range(1,len(self.foret)):
            if self.foret[i].frequence > self.foret[i-1].frequence:
                min = self.foret[i]
        return min
        del self.foret






if __name__ == "__main__":
    import doctest
    doctest.testmod()
    A = Arbre(18,
              Arbre(8,
                    Arbre(3,
                          Feuille(1, 'd'),
                          Feuille(2, 'c')),
                    Feuille(5, 'b')),
              Feuille(10, 'a'))
    A.affiche()
    print(frequences('ABRACADABRA'))

