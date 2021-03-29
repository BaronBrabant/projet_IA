Afin de charger le fichier .cpx et d'initialiser la carte vous devez fournir le chemin absolue du fichier a la fonction
map_generator(cpx_file) en le mettant en tant que parametre.
Pour l'instant le code accepte uniquement le fichier small.cpx!

Une fois le jeu lancer vous pouvez donner des instructions aux fourmis comme:

se déplacer:
ex: 18-19:@19-19 #la fourmi qui se trouve en 18-19 va se déplacer vers la case 19-19.

attaquer:
ex: 18-19:*19-19 #la fourmi qui se trouve en 18-19 va attaquer la fourmi en 19-19.

prendre une motte:
ex: 18-19: lift #la fourmi qui se trouve en 18-19 va prendre la motte sur cette même case.

déposer une motte :
ex: 18-19: drop #la fourmi qui se trouve en 18-19 va lâcher la motte sur cette même case.

Les ordres du  joueur controller par le IA execute ses ordres automatiquement
