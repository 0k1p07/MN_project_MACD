import pandas
import matplotlib.pyplot as plt


def ema(tab,StartIndex,N):
    alpha=2/(N+1)
    licznik=0
    mianownik=0

    for i in range(0,N+1):
        licznik+=pow((1-alpha),i)*tab[StartIndex+N-i]
        mianownik+=pow((1-alpha),i)
    return licznik/mianownik

def signal_tab(macdt,macd2,N):
    tab=[]
    for i in range(0,macd2+N):
        tab.append(0)
    for i in range(macd2+N,1000):
        signal_i=ema(macdt,i-N,N)
        tab.append(signal_i)
    return tab

def ema_tab(otwarcia,emaN):#35
    tab=[]
    for i in range(0,emaN):
        tab.append(0)
    for i in range(emaN,1000):
        ema_i=ema(otwarcia,i-emaN,emaN)
        tab.append(ema_i)
    return tab

def MACD(otw,emaN1,emaN2):
    ema1 = ema_tab(otw, emaN1)
    ema2 = ema_tab(otw, emaN2)
    tab=[]
    for i in range(0,emaN2):
        tab.append(0)
    for i in range(emaN2,1000):
        macd_i=ema1[i]-ema2[i]
        tab.append(macd_i)
    return tab

def graj(daty,daty_kupna,wartosci_kupna,daty_sprzedazy,wartosci_sprzedazy,wartosc_otwarcia):
    daty_operacji=[]
    ki=0
    si=0
    for D in daty:
        if ki<len(daty_kupna) and D == daty_kupna[ki]:
            daty_operacji.append(('K',daty_kupna[ki],wartosci_kupna[ki]))
            ki+=1
        elif si < len(daty_sprzedazy) and D == daty_sprzedazy[si]:
            daty_operacji.append(('S',daty_sprzedazy[si],wartosci_sprzedazy[si]))
            si+=1

    if daty_operacji[0][0]=='S':
        ilosc_akcji=1000
        pieniadze=0
    elif daty_operacji[0][0]=='K':
        ilosc_akcji = 0
        pieniadze = 1000*wartosc_otwarcia

    for o in daty_operacji:
        if o[0]=='S':
            if ilosc_akcji!=0:
                pieniadze=ilosc_akcji*o[2]
                ilosc_akcji=0
        elif o[0]=='K':
            if pieniadze != 0:
                ilosc_akcji=pieniadze/o[2]
                pieniadze=0

    return (pieniadze,ilosc_akcji)

def wskaznik_MACD(csvname,g_ema1,g_ema2,g_signal,rysuj_wykresy):
    csv_wig_20 = pandas.read_csv(csvname)
    otw = csv_wig_20['Otwarcie']
    daty=csv_wig_20['Data']

    macdtab=MACD(otw,g_ema1,g_ema2)
    signal=signal_tab(macdtab,g_ema2,g_signal)

    pkt_kupna_data=[]
    pkt_kupna_wartosc=[]
    pkt_sprzedazy_data=[]
    pkt_sprzedazy_wartosc=[]
    for i in range(g_ema2+g_signal+1,1000):
        dzien_poprzedni=macdtab[i-1]-signal[i-1]
        dzien_dzisiejszy=macdtab[i]-signal[i]
        if dzien_poprzedni>0 and dzien_dzisiejszy<=0:
            pkt_sprzedazy_data.append(daty[i])
            pkt_sprzedazy_wartosc.append(otw[i])
        elif dzien_poprzedni<0 and dzien_dzisiejszy>=0:
            pkt_kupna_data.append(daty[i])
            pkt_kupna_wartosc.append(otw[i])

    if(rysuj_wykresy==True):
        plt.plot(daty,otw,color='c',label='Wartość na otwarcie')
        plt.plot(daty,macdtab,color='b',label='MACD')
        plt.plot(daty,signal,color='m',label='Signal')
        plt.plot(pkt_kupna_data,pkt_kupna_wartosc,'g2',label='Punkty kupna')
        plt.plot(pkt_sprzedazy_data,pkt_sprzedazy_wartosc,'r2',label='Punkty sprzedaży')
        plt.legend(loc="upper right")
        plt.title(csvname)
        plt.show()


    wynik=graj(daty, pkt_kupna_data, pkt_kupna_wartosc, pkt_sprzedazy_data, pkt_sprzedazy_wartosc,otw[0])
    stan_koniec=wynik[0]+wynik[1]*otw[999]
    stan_pocz=1000*otw[0]
    zarobione=(stan_koniec/stan_pocz)
    return zarobione


def szukaj():
    najlepszy=(0,0,0,0)
    indeksik=0
    wyniki=[]
    for test_ema_1 in range(5,21):
        for test_roznica_ema1_ema2 in range(1,20):
            for test_ema_signal in range(5,16):
                wynik=wskaznik_MACD(test_ema_1,test_ema_1+test_roznica_ema1_ema2,test_ema_signal,False)
                wyniki.append((wynik,test_ema_1,test_ema_1+test_roznica_ema1_ema2,test_ema_signal))
                if najlepszy[0]<wynik:
                    najlepszy=(wynik,test_ema_1,test_ema_1+test_roznica_ema1_ema2,test_ema_signal)
                print(str(indeksik)+": "+str(test_ema_1)+" | "+str(test_ema_1+test_roznica_ema1_ema2)+" | "+str(test_ema_signal)+" --> "+str(wynik) + "("+str(najlepszy[0])+")")
                indeksik+=1
    print(najlepszy)
    wyniki.sort(reverse=True)
    print(wyniki[0:11])

#szukaj();
print(wskaznik_MACD("wig20_d2.csv",12,26,9,True))
print(wskaznik_MACD("10ply_b_d.csv",12,26,9,True))
print(wskaznik_MACD("btc_v_d.csv",12,26,9,True))
print(wskaznik_MACD("etc_v_d.csv",12,26,9,True))
print(wskaznik_MACD("tsla_us_d.csv",12,26,9,True))


print(wskaznik_MACD("wig20_d2.csv",7,26,6,True))
print(wskaznik_MACD("10ply_b_d.csv",7,26,6,True))
print(wskaznik_MACD("btc_v_d.csv",7,26,6,True))
print(wskaznik_MACD("etc_v_d.csv",7,26,6,True))
print(wskaznik_MACD("tsla_us_d.csv",7,26,6,True))

#print(wskaznik_MACD(7,26,6,False))