class Arbre:
    def __init__(self, frequence, gauche, droit, table={}):
        """ Construit un Arbre
            frequence: int
            gauche, droit: Arbre
        """
        self.frequence = frequence
        self.gauche = gauche
        self.droit = droit
        self.table = table

    def affiche(self, prefixes = ['    ']):
        """ Affiche l'arbre """
        print(''.join(prefixes[:-1]) + '|___' + str(self.frequence))
        prefixes.append('|   ')
        self.gauche.affiche(prefixes)
        prefixes.pop()
        prefixes.append('    ')
        self.droit.affiche(prefixes)
        prefixes.pop()

    def table_de_codage(self, code=''):
        '''
        permet de construire un dictionnaire qui associe à chaque symbole son code binaire
        :param code: string
        :return: dictionnaire -> {A:'0111', B:'1000111', ....}
        >>> H = Huffman(frequences("ABRACADABRA"))
        >>> H.arbre().table_de_codage()
        {'A': '0', 'C': '100', 'D': '101', 'B': '110', 'R': '111'}
        '''
        #Je precise que Nour m'a donner l'idée de m'inspirer de affiche() pour celle-ci ...
        #j'etais vraiment perdu après 4 heures de reflexion vaine sur la même fonction
        #du coup, on se retrouve avec la même fonction
        code += '0'
        self.gauche.table_de_codage(code)
        code = code[:-1]
        code += '1'
        self.droit.table_de_codage(code)

        return self.table

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

    def table_de_codage(self, code=''):
        '''
        permet de construire un dictionnaire qui associe à chaque symbole son code binaire
        Ici en particulier, le dictionnaire est mis à jour.
        :param code: string
        '''
        self.table[self.symbole] = code



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
    fréquence
    :param texte: str
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
        while self.fusion():
            pass


    def pop_min(self):
        """
        Retire la feuille avec la plus petite fréquence de la forêt et la retourne
        :return: Feuille
        """
        indice=0
        for i in range(1,len(self.foret)):
            if self.foret[i].frequence < self.foret[i-1].frequence:
                indice=i
        min = self.foret[indice]
        self.foret.pop(indice)
        return min


    def fusion(self):
        '''
        fusionne les 2 arbres de plus faible fréquence dans
        la foret
        :param self:
        :return: nothing
        '''
        if len(self.foret)>= 2 :
            gauche = self.pop_min()
            droit =  self.pop_min()
            frequence = gauche.frequence + droit.frequence
            nouveau = Arbre(frequence, gauche, droit)
            self.foret.append(nouveau)
            return True
        else : return False


    def arbre(self):
        '''
        retourne l'arbre de huffman après fusion !
        :return: Arbre
        >>> Huffman(frequences('ABRACADABRA')).arbre().frequence
        11
        '''
        return self.foret[0]

    def affiche(self):
        '''
        affiche l'arbre de Huffman créé
        :return:
        >>> freq = frequences("ABRACADABRA")
        >>> print(freq)
        {'A': 5, 'B': 2, 'R': 2, 'C': 1, 'D': 1}
        >>> H = Huffman(freq)
        >>> H.affiche()
        |___11
            |___5(A)
            |___6
                |___2
                |   |___1(C)
                |   |___1(D)
                |___4
                    |___2(B)
                    |___2(R)
        '''
        self.arbre().affiche()

    def compresse(self,texte):
        '''
        Permet de coder un texte selon la table de codage de Huffman, c'est à dire le compresser
        :param texte: string , ex : 'JOADIOAND'
        :return: string , ex: '1001101011001101110000111101010111'
        >>> H = Huffman(frequences("ABRACADABRA"))
        >>> H.compresse("ABRACADABRA")
        '01101110100010101101110'
        '''
        dict = self.arbre().table_de_codage()
        texte_compresse = ''
        for car in texte:
            texte_compresse += dict[car]
        return texte_compresse

    def decompresse(self,texte):
        '''
        permet de retrouver le texte original à partir
        :param texte: string , ex: '1001010010010011101'
        :return: string , ex: 'EJFIEJHF'
        >>> H = Huffman(frequences("ABRACADABRA"))
        >>> H.compresse("ABRACADABRA")
        '01101110100010101101110'
        >>> H.decompresse("01101110100010101101110")
        'ABRACADABRA'
        '''
        dict = self.arbre().table_de_codage()
        code=''
        texte_decode = ''
        for car in texte:
            code += car
            if code in [valeur for valeur in dict.values()]:
                texte_decode += [clef for clef in dict.keys() if dict[clef] == code][0]
                # Cette comprehension de liste permet de trouver toutes les clefs correspondant
                # au code, dans notre cas, il y a une bijection entre codes et clefs donc un seul élément
                # dans cette liste
                code = ''
        return texte_decode



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

    '''                                      QUESTION 11 :

    L'arbre de Huffman génère une table efficace car elle atribue au symbole de haute 
    fréquence les codes les plus cours (composés du moins de bit possible) 
    et inversement les symboles les moins fréquents sont nécéssairement associés
    aux codes les plus longs puisqu'ils sont fusionnés au départ.
    '''

    #---------------------------------------QUESTION 12--------------------------------------------------
    print(encode_ascii('ABRACADABRA'))
    print(Huffman(frequences("ABRACADABRA")).compresse('ABRACADABRA'))
    print(len(encode_ascii('ABRACADABRA'))/len(Huffman(frequences("ABRACADABRA")).compresse('ABRACADABRA')))
    #On trouve un facteur de compression de 3.83 ! Evidemment la compression est
    #très efficace car notre Huffman a été initialisé avec le texte 'ABRACADABRA'
    #que l'on voulait compresser


