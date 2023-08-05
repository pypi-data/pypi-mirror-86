class A():
    ## مرحباً بالضوء، كيف أحوالك؟
    '''# To use:
    APL.Reshape_Arabic(Any text, To reverse type #True#)'''
    def Reshape_Arabic(text = '', reverse = False):
        harakat = "ًٌٍَُِّْ"
        list1 = 'ئبتثجحخسشصضطظعغفقكلمنهي'
        list2 = 'آأؤإاةدذرزوى'
        list3 = 'ء '
        v = 0

        reshaped_text = ''
        textlist = list(' '+text+' ') #هذه الخطوة ضرورية ليعمل الكود بشكل صحيح

        letters_Table = {'''  '<initial>' '<medial>' '<final>' '<isolated>' '''
                        "ء" : [u"\ufe80", u"\ufe80", u"\ufe80", u"\ufe80"], #ء  Xإن محيت الهمزة من هنا فستحدث مشكلة
                        "آ" : [u"\ufe81", u"\ufe82", u"\ufe82", u"\ufe81"], #آ
                        "أ" : [u"\ufe83", u"\ufe84", u"\ufe84", u"\ufe83"], #أ
                        "ؤ" : [u"\ufe85", u"\ufe86", u"\ufe86", u"\ufe85"], #ؤ
                        "إ" : [u"\ufe87", u"\ufe88", u"\ufe88", u"\ufe87"], #إ
                        "ئ" : [u"\ufe8b", u"\ufe8c", u"\ufe8a", u"\ufe89"], #ئ
                        "ا" : [u"\ufe8d", u"\ufe8e", u"\ufe8e", u"\ufe8d"], #ا
                        "ب" : [u"\ufe91", u"\ufe92", u"\ufe90", u"\ufe8f"], #ب
                        "ة" : [u"\ufe93", u"\ufe94", u"\ufe94", u"\ufe93"], #ة
                        "ت" : [u"\ufe97", u"\ufe98", u"\ufe96", u"\ufe95"], #ت
                        "ث" : [u"\ufe9b", u"\ufe9c", u"\ufe9a", u"\ufe99"], #ث
                        "ج" : [u"\ufe9f", u"\ufea0", u"\ufe9e", u"\ufe9d"], #ج
                        "ح" : [u"\ufea3", u"\ufea4", u"\ufea2", u"\ufea1"], #ح
                        "خ" : [u"\ufea7", u"\ufea8", u"\ufea6", u"\ufea5"], #خ
                        "د" : [u"\ufea9", u"\ufeaa", u"\ufeaa", u"\ufea9"], #د
                        "ذ" : [u"\ufeab", u"\ufeac", u"\ufeac", u"\ufeab"], #ذ
                        "ر" : [u"\ufead", u"\ufeae", u"\ufeae", u"\ufead"], #ر
                        "ز" : [u"\ufeaf", u"\ufeb0", u"\ufeb0", u"\ufeaf"], #ز
                        "س" : [u"\ufeb3", u"\ufeb4", u"\ufeb2", u"\ufeb1"], #س
                        "ش" : [u"\ufeb7", u"\ufeb8", u"\ufeb6", u"\ufeb5"], #ش
                        "ص" : [u"\ufebb", u"\ufebc", u"\ufeba", u"\ufeb9"], #ص
                        "ض" : [u"\ufebf", u"\ufec0", u"\ufebe", u"\ufebd"], #ض
                        "ط" : [u"\ufec3", u"\ufec4", u"\ufec2", u"\ufec1"], #ط
                        "ظ" : [u"\ufec7", u"\ufec8", u"\ufec6", u"\ufec5"], #ظ
                        "ع" : [u"\ufecb", u"\ufecc", u"\ufeca", u"\ufec9"], #ع
                        "غ" : [u"\ufecf", u"\ufed0", u"\ufece", u"\ufecd"], #غ
                        "ف" : [u"\ufed3", u"\ufed4", u"\ufed2", u"\ufed1"], #ف
                        "ق" : [u"\ufed7", u"\ufed8", u"\ufed6", u"\ufed5"], #ق
                        "ك" : [u"\ufedb", u"\ufedc", u"\ufeda", u"\ufed9"], #ك
                        "ل" : [u"\ufedf", u"\ufee0", u"\ufede", u"\ufedd"], #ل
                        "م" : [u"\ufee3", u"\ufee4", u"\ufee2", u"\ufee1"], #م
                        "ن" : [u"\ufee7", u"\ufee8", u"\ufee6", u"\ufee5"], #ن
                        "ه" : [u"\ufeeb", u"\ufeec", u"\ufeea", u"\ufee9"], #ه
                        "و" : [u"\ufeed", u"\ufeee", u"\ufeee", u"\ufeed"], #و
                        "ى" : [u"\ufeef", u"\ufef0", u"\ufef0", u"\ufeef"], #ى
                        "ي" : [u"\ufef3", u"\ufef4", u"\ufef2", u"\ufef1"], #ي
        }

        for i in range(1, len(textlist)-1):
            #تقرير إن كان الحرف متصلا بما قبله أم لا
            aroundbefore = 1
            while textlist[i-aroundbefore] in harakat:
                aroundbefore += 1
            if textlist[i-aroundbefore] in list1:
                before = 1
            else:
                before = 0

            #تقرير إن كان الحرف متصلا بما بعده أم لا
            aroundafter = 1
            while textlist[i+aroundafter] in harakat:
                aroundafter += 1
            if textlist[i] in list1 and textlist[i+aroundafter] in list1 or textlist[i] in list1 and textlist[i+aroundafter] in list2:
                after = 1
            else:
                after = 0

            if textlist[i] not in letters_Table: #إن لم يكن في الجدول
                if textlist[i] == 'ء':  #وضعت الهمزة هنا لأنها لم تعمل في الجدول
                    new_text = u"\ufe80"
                else:
                    new_text = textlist[i]  #إن لم يكن في الجدول اترك الحرف كما هو
            else:
                #إن كان في الجدول فحدد شكله
                if before == 0 and after == 1: #أول الكلمة
                    new_text = letters_Table[textlist[i]][0]
                if before == 1 and after == 1: #وسط الكلمة
                        new_text = letters_Table[textlist[i]][1]
                if before == 1 and after == 0: #آخر الكلمة
                    new_text = letters_Table[textlist[i]][2]
                if before == 0 and after == 0: #منفصل
                    new_text = letters_Table[textlist[i]][3]

            reshaped_text += str(new_text)  #أضف الحرف لمتغير واحد
            new_text = ''   #ارجع قيمة المتغير الذي يأخذ قيمة الحرف عدما كي لا تتراكم الأحرف فيه

        #لاستبدال الألف واللام المنفصلين بحرف متصل
        reshaped_text = reshaped_text.replace('ﻟﺂ', 'ﻵ')
        reshaped_text = reshaped_text.replace('ﻠﺂ', 'ﻶ')
        reshaped_text = reshaped_text.replace('ﻟﺄ', 'ﻷ')
        reshaped_text = reshaped_text.replace('ﻠﺄ', 'ﻸ')
        reshaped_text = reshaped_text.replace('ﻟﺈ', 'ﻹ')
        reshaped_text = reshaped_text.replace('ﻠﺈ', 'ﻺ')
        reshaped_text = reshaped_text.replace('ﻟﺎ', 'ﻻ')
        reshaped_text = reshaped_text.replace('ﻠﺎ', 'ﻼ')

        #لعكس النص
        if reverse == True:
            reshaped_text = reshaped_text[::-1]

        return reshaped_text
        '''Output is a text'''

    ##--------------------------------------------------------------------------------------------------------------------------------------##

    '''# To use:
    APL.Extract(Any text, Before the wanted text, After the wanted text, Wanted text min size, Wanted text max size)'''
    def Extract(text, before, after, min = False, max = False):
        # المتغيرات
        English_Letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
        Symbols = '1234567890-=!"£$%^&*()_+`[];"@\|:~{}<>?./,# ' + "'"
        extract, same = False, False
        ExText, line = [], ''
        
        text = text.replace(before, u'\uFFFE')
        if before != after: text = text.replace(after, u'\uFFFF')
        else: same = True
        
        # استخراج النصوص
        for char in text:
            if ((char == u'\uFFFF' and same == False) or (char == u'\uFFFE' and same == True)) and extract == True:
                extract = False
                
                # التحقق من طول النص وتناسبه مع شروط الطول
                if min != False:
                    if len(line) < min:
                        line = ''
                if max != False:
                    if len(line) > max:
                        line = ''
                
                if line != '':
                    ExText.append(line)
                    line = ''
            
            if extract == True:
                if char in English_Letters or char in Symbols: #لإبقاء فقط النصوص التي كل أحرفها في English_Letters أو Symbols
                    line += char
                else:
                    line = ''
                    extract = False
            
            if char == u'\uFFFE':
                extract = True
                line = ''
        return ExText
        '''Output is an array'''

    ##--------------------------------------------------------------------------------------------------------------------------------------##

    '''# To use:
    APL.Text_Box_Fitter(Any text, Text zone width, Lines number, New line command, New page command, Characters list: [[char 1, width], [char2, width]...])'''
    def Text_Box_Fitter(Input_text, text_zone_width, lines_num, new_line_command, new_page_command, Chars):
        #تفقد المعطيات
        #---------------------------------------------
        Errors = ''
        c = False

        if text_zone_width != 0:
            for mini_list in Chars:
                if mini_list[1] > text_zone_width:
                    if c == False:
                         Errors += 'Error 00:\n'
                         c = True
                    Errors += chr(mini_list[0]) + ' is wider than text_zone.\n'

        if text_zone_width == 0:
            if c == True: Errors += '\n'
            Errors += "Error 01:\ntext_zone_width can't be 0.\n"
            if c == False: c = True

        if lines_num == 0:
            if c == True: Errors += '\n'
            Errors += "Error 02:\nlines_num can't be 0.\n"
            if c == False: c = True

        if c == True:
            print(Errors)
            exit()

        #هنا يبدأ العمل الجاد
        #---------------------------------------------
        text_zone_width += 1
        lines_num -= 2
        text = A.Reshape_Arabic(Input_text, False)
        new_text = ''
        X, Y = 0, 0

        word = ''
        text_list = []
        for char in text:
            if char != ' ': word += char
            else:
                text_list.append(word)
                text_list.append(' ')
                word = ''
        text_list.append(word)
        word = ''

        for item in text_list:
            item_len = 0
                
            for char in item:
                found = False
                for mini_list in Chars:
                    if ord(char) == mini_list[0]:
                        item_len += mini_list[1]
                        found = True
                        break
                if found == False:
                    print('Error 03:\nchar ("' + char + '" , ' + str(ord(char)) + ') not found in table.')
                    exit()
                
            if X + item_len > text_zone_width and text_zone_width > item_len:
                if Y <= lines_num:
                    new_text += new_line_command
                    Y += 1
                else:
                    new_text += new_page_command
                    Y = 0
                X = 0
                
            for char in item:
                found = False
                for mini_list in Chars:
                    if ord(char) == mini_list[0]:
                        if text_zone_width - X < mini_list[1]:
                            if Y <= lines_num:
                                new_text += new_line_command
                                Y += 1
                            else:
                                new_text += new_page_command
                                Y = 0
                            X = 0
                        X += mini_list[1]
                        new_text += char
                        found = True
                        break
                if found == False:
                    print('Error 03:\nchar ("' + char + '" , ' + str(ord(char)) + ') not found in table.')
                    exit()

        R = new_line_command + ' '
        for R in new_text:
            new_text = new_text.replace(new_line_command + ' ', new_line_command)
        R = ' ' + new_line_command
        for R in new_text:
            new_text = new_text.replace(' ' + new_line_command, new_line_command)
        R = new_page_command + ' '
        for R in new_text:
            new_text = new_text.replace(new_page_command + ' ', new_page_command)
        R = ' ' + new_page_command
        for R in new_text:
            new_text = new_text.replace(' ' + new_page_command, new_page_command)
        R = new_line_command + new_line_command
        for R in new_text:
            new_text = new_text.replace(new_line_command + new_line_command, new_line_command)
        R = new_page_command + new_page_command
        for R in new_text:
            new_text = new_text.replace(new_page_command + new_page_command, new_page_command)

        #إعادة النتيجة
        #---------------------------------------------
        return new_text
        '''Output is a text'''
        
    ##--------------------------------------------------------------------------------------------------------------------------------------##
