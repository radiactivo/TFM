from utils import find
from time import sleep
import pdb
import os

dir_project = '/Users/radiactivo/Documents/TFM/'
dir_samples = dir_project + 'samples/'
dir_mutated = dir_project + 'mutated/'

files = find('*.vcf', dir_samples)

seeds = [764225987, 328117335, 454487956, 748305375, 260137859, 1243806, 3044198, 3588851, 3833722, 5083748, 16613091, 18875760, 20038906, 20614116, 22037110, 22955802, 23157467, 24610293, 29712771, 31583379, 32470783, 33337195, 34364287, 35590319, 37148420, 37991366, 38402152, 38944855, 40939231, 41015714, 43021718, 44588180, 48419588, 48673550, 53179392, 53731190, 56590076, 57528731, 64699203, 65204904, 67752520, 76342450, 77383820, 77859513, 80151477, 80457641, 82782220, 86252879, 99043440, 100052973, 100837714, 103789359, 104300683, 112008884, 113306048, 115574104, 117366951, 118977950, 119085670, 119508115, 121162655, 122232122, 123443020, 123722000, 124563536, 126551069, 127649132, 129675272, 129684584, 133373745, 134752938, 137795690, 138140814, 141146194, 141825389, 141876711, 143536169, 144115338, 144768151, 145159038, 145739777, 146052453, 146242439, 147084883, 147817407, 147884908, 148226254, 149007700, 151082651, 152764296, 154199116, 155062140, 157519812, 157878583, 158301125, 163715906, 167864670, 168683404, 170553641, 171605801, 172304891, 175568959, 176409086, 178218108, 180024636, 180359278, 182217062, 182673531, 185205074, 186493863, 186966529, 188980874, 189018052, 189415791, 189827451, 190922659, 200234038, 202431255, 204322628, 208590415, 209429905, 209570652, 212958413, 214028368, 219774078, 224570936, 229089820, 235150172, 237143521, 243042240, 244018477, 245653641, 249059893, 250890694, 260458194, 261824961, 261900483, 262879424, 263326382, 263739165, 266973801, 267134058, 267518561, 269017906, 272454541, 273247123, 273468928, 273731653, 274702983, 277049293, 280978235, 281194761, 283011555, 283347295, 285448607, 286219701, 287887052, 288842585, 291460962, 292195570, 294181985, 294951547, 299356101, 299483329, 305792188, 305815261, 307095374, 307430961, 308318646, 311193961, 315542254, 315960944, 318343746, 319269791, 319745554, 323671700, 324275359, 324620449, 326514751, 326759092, 327065353, 327187315, 327977486, 329178504, 330578027, 330611410, 331202268, 333048443, 334113950, 334188187, 336620189, 337224271, 339574114, 340058785, 340390930, 343701927, 346230276, 357230890, 361409102, 362957799, 364793148, 368941294, 371004572, 373939979, 376736595, 381814060, 389349037, 389745509, 395049046, 395619071, 397276425, 398977429, 399048400, 399088705, 400430037, 404580433, 408764976, 408877916, 409873132, 413779631, 414597112, 414950552, 415441544, 417489772, 419645775, 421031916, 424061162, 429374000, 429959944, 432448301, 433156158, 435916871, 435926614, 438148195, 442427987, 443901994, 444588019, 445453263, 447565732, 453363666, 456100635, 457898729, 459345627, 461527710, 463958223, 472749928, 475315782, 482890705, 487400250, 488096900, 491426170, 491504159, 494475261, 494937074, 495310814, 497520020, 498270855, 499989305, 500239038, 501640455, 503583375, 503649010, 507494961, 508459031, 511268546, 513194530, 514805546, 515082639, 515102758, 517271632, 518088142, 518385987, 519785753, 520046714, 521897012, 524910799, 525951052, 527245877, 532876686, 536676445, 539844146, 541128251, 541451836, 542940884, 544832766, 547806935, 549747328, 551109657, 553728125, 557865220, 558386763, 561583580, 566536338, 566650077, 573006849, 574741378, 576942002, 579041883, 579516418, 581957195, 582250218, 582663226, 586009034, 587327230, 587339374, 587431019, 588898110, 589411444, 598776060, 608671106, 609887979, 610661820, 611631683, 612469944, 614404310, 616770401, 620050506, 621678564, 622007005, 624569528, 625652504, 626184320, 629565732, 634191686, 639047200, 643382448, 645992262, 650755036, 655092193, 655422922, 661231384, 662858296, 664456254, 669485984, 671183307, 674403747, 678391039, 685122354, 685147715, 685384582, 686047890, 689666107, 698617431, 702063445, 707858354, 711055312, 711747308, 711836639, 715402576, 717412362, 718414696, 719017068, 720662178, 726213142, 730414657, 733574748, 734745236, 739138421, 741196258, 743369426, 746461075, 746889314, 751942188, 757487845, 759613334, 760618238, 762097878, 762494608, 763556672, 765043277, 766782592, 768256295, 769390291, 771028052, 772610801, 772904637, 773228216, 773441799, 777261165, 778518724, 781335883, 782271176, 786047760, 786705734, 788580210, 793591822, 793799890, 795089066, 799025537, 801974407, 802528293, 804324279, 808742889, 808769359, 811397056, 811763464, 812252992, 812836323, 813798928, 814910077, 816565215, 816963656, 818796044, 819056797, 819436132, 819482892, 820590125, 822372093, 823543178, 823621066, 825653018, 830717412, 832955907, 837121809, 837690448, 838279020, 839067193, 843524343, 844772460, 846437960, 847126443, 847426360, 848217373, 849877307, 851711133, 855808049, 856259746, 857938341, 860491402, 862684949, 864255924, 867538036, 868065600, 868091672, 869216857, 870246135, 871723229, 875784713, 876103969, 877968724, 878853455, 880854674, 881726051, 883365248, 883440486, 885058147, 885820033, 888789862, 890841482, 895152834, 897265283, 905222965, 905454277, 906495026, 907693238, 909945653, 910168205, 912389539, 913148324, 915543128, 920001869, 920735667, 922403084, 922413285, 923621014, 924091066, 924337381, 926992016, 928284858, 928854814, 930630413, 931276126, 932447787, 935716995, 935727454, 939796302, 942122862, 944640514, 944793461, 945103711, 946677068, 946753086, 947248850, 949793633, 950634047, 955243211, 956879575, 958378548, 958806081, 958899436, 959478107, 962289183, 963525967, 965580232, 971081065, 973162963, 983502460, 985513545, 985967803, 992839359, 992886928, 993037710, 993939321, 998130470, 998507251]

fuz_num = 0
for file in files:
	for seed in seeds:
		os.system('radamsa -s ' + str(seed) + ' ' + dir_samples + file.split('/')[-1] + ' > ' + dir_mutated + 'fuzzed_' + str(fuz_num) + '.vcf')
		fuz_num += 1

fuzs = find('*vcf', dir_mutated)

for fuz in fuzs:
	os.system('adb push ' + fuz + ' /sdcard/vcfs/' + fuz.split('/')[-1])

for fuz in fuzs:
	os.system('adb shell am start -t "text/x-vcard" -d "file:///sdcard/vcfs/' + fuz.split('/')[-1] + '" -a android.intent.action.VIEW com.android.contacts')
	os.system('adb shell input keyevent 61')
	os.system('adb shell input keyevent 23')
	sleep(2)
