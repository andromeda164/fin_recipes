""" ******************************************************

    Berechnung von Quasi-Zufallszahlen nach Sobol.
    Referenz: NR, sobseq()
    
    Beschreibung:   Berechnung von Quasi-Zufallszahlen
                    nach Sobl, Variante Antonov-Saleev.

                    Die Funktion gibt ein Tupel mit den
                    folgenden Werten zurueck:


    Argumente       Python-Typ  Beschreibung
    ---------------------------------------------------------
    n               int         xxxx

    Status
    ------------------------------------------------------
    Syntax          --
    Numerisch       --
    Testprogramm    --
    Literatur       --         
*******************************************************"""

MAXBIT = 30
MAXDIM = 6

def sobseq(n, x):
    'returns the Sobol quasi-random number sequence x[1,.. n] for n dimensions.'
    j, k, l = 0, 0 ,0
    i, im, ipp = 0L, 0L, 0L
    fac = 0.0
    _in = 0L
    ix = [0L for _x in range(MAXDIM+1)]
    iu = [0L for _x in range(MAXBIT+1)]
    mdeg = [0L, 1L, 2L, 3L, 3L, 4L, 4L]
    ip = [0L, 0L, 1L, 2L, 1L, 4L]
    iv = [0] * (MAXBIT*MAXDIM+1)
    iv[0:25] = [0,1,1,1,1,1,1,3,1,3,3,1,1,5,7,7,3,3,5,15,11,5,15,13,9]

    if n<0:
        # Initialize, don't return a record
        for k in range(1,MAXDIM+1):
            ix[k] = 0L
        _in = 0L
        if iv[1] != 1:
            return
        fac = 1.0 / (1L << MAXBIT)
        k = 0
        j = 1
        while j<=MAXBIT:
            iu[j] = iv[k]
            j += 1
            k += MAXDIM
        for k in range(1, MAXDIM+1):
            for j in range(1, mdeg[k]+1):
                iu[j][k] = iu[j][k] << (MAXBIT - j)
            # stored values only require normalization
            for j in range(mdeg[k]+1,MAXBIT+1):
                ipp = ip[k]
                i = iu[j-mdeg[k]][k]
                i ^= (i >> mdeg[k])
                for l in range(mdeg[k]-1, 0, -1):
                    if (ipp & 1):
                        i ^= iu[j-l][k]
                    ipp >>= 1
                iu[j][k] = i
    else:
        im = _in
        _in += 1
        for j in range(1, MAXBIT+1):
            if not (im & 1): break
            im >>= 1
        if j > MAXBIT: raise 'MAXBIT too small in sobseq!'
        im = (j-1)*MAXDIM
        for k in range(1, min(n, MAXDIM)+1):
            ix[k] ^= iv[im+k]
            x[k] = ix[k]*fac

if __name__=='__main__':
    dimension = 2
    length = 10
    l = [0.0]*dimension
    sobseq(-1, l)
    print sobseq(dimension, l)
    print sobseq
