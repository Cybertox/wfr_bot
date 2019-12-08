def ratioGenerator(reviewed, accepted, rejected, duplicated):
    medals = [['none', 0, "https://raw.githubusercontent.com/Cybertox/decypher_bot/master/wfr_logo.png"],
              ['Bronze', 100, "https://dedo1911.xyz/Badges/Badge_OPR_Silver.png"],
              ['Silver', 750, "https://dedo1911.xyz/Badges/Badge_OPR_Gold.png"],
              ['Gold', 2500, "https://dedo1911.xyz/Badges/Badge_OPR_Gold.png"],
              ['Platinum', 5000, "https://dedo1911.xyz/Badges/Badge_OPR_Platinum.png"],
              ['Onyx', 10000, "https://dedo1911.xyz/Badges/Badge_OPR_Black.png"]]
    ratio = (accepted + rejected+duplicated)/reviewed
    agreements = accepted + rejected + duplicated
    limbo = reviewed - agreements
    badge = medals[0]
    if agreements >= medals[5][1]:
        badge = medals[5]
    elif agreements >= medals[4][1]:
        badge = medals[4]
    elif agreements >= medals[3][1]:
        badge = medals[3]
    elif agreements >= medals[2][1]:
        badge = medals[2]
    elif agreements >= medals[1][1]:
        badge = medals[1]
    else:
        badge = medals[0]
    next = 0
    nextBadge = 'none'
    badgeUrl = ""
    for i in range(len(medals)-1):
        if badge == medals[i] and (badge != medals[5]):
            next = medals[i+1][1] - agreements
            nextBadge = medals[i+1][0]
            badgeUrl = medals[i][2]
        elif badge == medals[5]:
            next = 0
            badgeUrl = medals[i][2]
    return [agreements, ratio, limbo, badge[0], next, nextBadge, badgeUrl]

def dataGenerator(spl_text):
    reviewed, accepted, rejected, duplicated = 0, 0, 0, 0
    for i in range(len(spl_text)):
        if spl_text[i].startswith('Reviewed'):
            if spl_text[i].lstrip('Reviewed').isdecimal():
                reviewed = int(spl_text[i].lstrip('Reviewed'))
            elif spl_text[i].lstrip('Reviewed') == "":
                reviewed = int(spl_text[i + 1])

        if spl_text[i].startswith('Accepted'):
            if spl_text[i].lstrip('Accepted').isdecimal():
                accepted = int(spl_text[i].lstrip('Accepted'))
            elif spl_text[i].lstrip('Accepted') == "":
                accepted = int(spl_text[i + 1])

        if spl_text[i].startswith('Rejected'):
            if spl_text[i].lstrip('Rejected').isdecimal():
                rejected = int(spl_text[i].lstrip('Rejected'))
            elif spl_text[i].lstrip('Rejected') == "":
                rejected = int(spl_text[i + 1])

        if spl_text[i].startswith('Duplicated'):
            if spl_text[i].lstrip('Duplicated').isdecimal():
                duplicated = int(spl_text[i].lstrip('Duplicated'))
            elif spl_text[i].lstrip('Duplicated') == "":
                duplicated = int(spl_text[i + 1])
    return [reviewed, accepted, rejected, duplicated]


