function checkWinner(list) {

    if (list.includes("0") && list.includes("1") && list.includes("2")) {
        $('#line-h-1').show()
        winner = true
        return winner
    }
    else if (list.includes("3") && list.includes("4") && list.includes("5")) {
        $('#line-h-2').show()
        winner = true
        return winner
    }
    else if (list.includes("6") && list.includes("7") && list.includes("8")) {
        $('#line-h-3').show()
        winner = true
        return winner
    }
    else if (list.includes("0") && list.includes("3") && list.includes("6")) {
        $('#line-v-1').show()
        winner = true
        return winner
    }
    else if (list.includes("1") && list.includes("4") && list.includes("7")) {
        $('#line-v-2').show()
        winner = true
        return winner
    }
    else if (list.includes("2") && list.includes("5") && list.includes("8")) {
        $('#line-v-3').show()
        winner = true
        return winner
    }
    else if (list.includes("2") && list.includes("4") && list.includes("6")) {
        $('#line-righttoleft').show()
        winner = true
        return winner
    }

    else if (list.includes("0") && list.includes("4") && list.includes("8")) {
        $('#line-lefttoright').show()
        winner = true
        return winner
    }
}