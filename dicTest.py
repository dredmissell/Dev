#a = ["one", "two", "two", "three", "four", "five", "five", "five", "six"]
bbs = []


bbsIntersect1 = {'FID': 0, 'rtestopNo': '1111-1', 'hucId': '0404', 'interSectArea': .1567}
bbs.append(bbsIntersect1)
bbsIntersect2 = {'FID': 1,'rtestopNo': '1111-2', 'hucId': '0404', 'interSectArea': .1267}
bbs.append(bbsIntersect2)
bbsIntersect3 = {'FID': 2,'rtestopNo': '1111-3', 'hucId': '0406', 'interSectArea': .1167}
bbs.append(bbsIntersect3)
bbsIntersect4 = {'FID': 3, 'rtestopNo': '1111-4', 'hucId': '0405', 'interSectArea': .1967}

bbsIntersect5 = {'FID': 4, 'rtestopNo': '1111-5', 'hucId': '0405', 'interSectArea': .3967}

test = len(bbs)
for d in bbs:
    bbsId = bbsIntersect5['rtestopNo']
    if bbsIntersect5['rtestopNo'] in d.itervalues():
        # comparison logic -- keep the poly with the largest intersection area
        if bbsIntersect4['interSectArea'] > bbsIntersect1['interSectArea']:
            # get the current bbsId
            curId = d['rtestopNo']
            # remove the old entry
            bbs.remove(d)
            # add the new entry
            bbs.append(bbsIntersect4)
    else:
        # if the bbs is not int eh dictionary add it
        bbs.append(bbsIntersect4)
print bbs


# valueList=bbsIntersect1.values()
# print valueList
#
# if not any(d['bbsId'] == bbsVal for d in bbs):
#
# for a in bbs:
#     for b in bbsIntersect2:
#         if bbsIntersect1


# valueList.sort()
# valueList.reverse()
#
#
#
# for num in bbs:
#     keyList.append(get_Value(dic,num))
#
#
# dic = {}
# for name in a:
#     if name in dic:
#         dic[name] = dic[name]+1
#     else:
#         dic[name] = 1
#
# keyList = []
# valueList=dic.values()
# valueList.sort()
# valueList.reverse()
#
# def get_Value(dic,value):
#     for name in dic:
#         if dic[name] == value:
#             del dic[name]
#             return name
#
#
# for num in valueList:
#     keyList.append(get_Value(dic,num))
#
# print keyList

# bbsIntersect['bbsId'] = bbsVal
# bbsIntersect['hucId'] = hucVal
# bbsIntersect['interSectArea'] = interSectArea
# bbs.append(bbsIntersect)