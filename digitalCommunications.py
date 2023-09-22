import random

# Βοηθητική συνάρτηση που πραγματοποιεί διαίρεση με αριθμητική modulo-2
def modulo2_division(dividend, divisor):
    current_pos = 0
    dividend_list = list(dividend)

    while current_pos <= len(dividend) - len(divisor):
        for i in range(len(divisor)):
            dividend_list[current_pos + i] = str(int(dividend_list[current_pos + i]) ^ int(divisor[i]))

        while current_pos < len(dividend) and dividend_list[current_pos] == '0':
            current_pos += 1

    remainder = ''.join(dividend_list[current_pos:])
    return remainder



# ΜΑΙΝ

k = 20
p = "110101"
# p = input("Δώσε το p: ")
ber = 10**(-3)
n = len(p)+k-1

DEBUG = False

countIsTrulyWrong = 0
countMaybeWrong = 0
countDidntFind = 0

times = 1000


with open("statistics.csv", "w", encoding="utf-8") as out:
    separator = ", "
    # Εάν ανοίξετε το αρχείο σε excel, αλλάξτε τον separator σε ";", δηλ:
    #separator = "; "
    out.write("Αρχικό σήμα" + separator + "FCS" + separator + "Σήμα προς αποστολή" + separator + "Λαμβανόμενο σήμα" + separator + "Έλεγχος από τον αλγόριθμο" + separator + "Πραγματικός έλεγχος" + separator + "Bits που αλλοιώθηκαν" + "\n")

    for i in range(times):
        # Κατασκευή ενός σήματος μήκους k με τυχαία bits.
        originalSignal = "".join([str(random.randint(0, 1)) for i in range(k)])
        if DEBUG: print("Το αρχικό σήμα:", originalSignal)
        out.write(originalSignal + separator)

        # Προσθήκη των μηδενικών που χρειάζονται για την πραγματοποίηση της διαίρεσης.
        tempSignal = originalSignal + "0" * (n-k)

        # Υπολογισμός του FCS κάνοντας διαίρεση modulo-2 του tempSignal (με τα μηδενικά στο τέλος) και του p.
        fcs = modulo2_division(tempSignal, p)
        fcs = "0"*(n-k-len(fcs)) + fcs
        if DEBUG: print("FCS:", fcs)
        out.write(fcs + separator)

        # Δημιουργούμε το μήνυμα προς αποστολή ως το αρχικό μήνυμα και τα ψηφία του fcs στο τέλος του μηνύματος.
        signalToSend = originalSignal + fcs
        if DEBUG: print("Το μήνυμα προς αποστολή:", signalToSend)
        out.write(signalToSend + separator)

        # Προσομοίωση αποστολής μηνύματος: αλλοιώνουμε μερικά bits με βάση τη πιθανότητα που ορίσαμε (ber)
        receivedMessage = "".join([signalToSend[i] if random.random() > ber else str(int(not bool(signalToSend[i]))) for i in range(len(signalToSend))])
        if DEBUG: print("Το λαμβανόμενο μήνυμα:", receivedMessage)
        out.write(receivedMessage + separator)

        # Ελέγχουμε αν το ληφθέν μήνυμα διαρείται ακριβώς με το p (δηλαδή είναι σωστό). Εδώ κάνουμε μία παραδοχή πως το 0 υπόλοιπο της διαίρεσης συμβολίζεται με την κενή συμβολοσειρά.
        seemsToBeRight = modulo2_division(receivedMessage, p) == ""
        if not seemsToBeRight: countMaybeWrong = countMaybeWrong + 1
        if DEBUG: print("Έλεγχος βάσει αλγορίθμου ανίχνευσης σφαλμάτων του μηνύματος που στάλθηκε και παραλήφθηκε:", seemsToBeRight)
        out.write(str(seemsToBeRight) + separator)

        # Ελέγχουμε αν στην πραγματικότητα τα δύο μηνύματα ήταν ίσα.
        isTrulyRight = signalToSend == receivedMessage
        if not isTrulyRight: countIsTrulyWrong = countIsTrulyWrong + 1
        if DEBUG: print("Έλεγχος πραγματικής ισότητας μηνύματος που στάλθηκε και παραλήφθηκε:", isTrulyRight)
        out.write(str(isTrulyRight) + separator)

        # Σε περίπτωση που δεν ήταν πραγματικά ίσα, τότε υπολογίζουμε πόσα bits αλλοιώθηκαν.
        if not isTrulyRight:
            notSameCharacters = sum(c1 != c2 for c1, c2 in zip(signalToSend, receivedMessage))
            if DEBUG: print("Bits που αλλοιώθηκαν:", notSameCharacters)
            out.write(str(notSameCharacters))
        else:
            out.write("0")

        if not isTrulyRight and seemsToBeRight: countDidntFind = countDidntFind + 1
        
        out.write("\n")
        
       

    if DEBUG: print()
    print("Τα μηνύματα που έφτασαν πραγματικά εσφαλμένα στον αποδέκτη ήταν:", countIsTrulyWrong/times*100, "\b%")
    print("Τα μηνύματα που ανιχνεύτηκαν ως εσφαλμένα στον αποδέκτη ήταν:", countMaybeWrong/times*100, "\b%")
    print("Τα μηνύματα που έφτασαν πραγματικά εσφαλμένα αλλά δεν ανινεύτηκαν στον αποδέκτη ήταν:", countDidntFind/times*100, "\b%")
    print("Αναλυτικά τα δεδομένα κατά την εκτέλεση παρουσιάζονται στο αρχείο \"statistics.csv\" που δημιουργείται στον φάκελο κάθε φορά που εκτελείται ο αλγόριθμος.")