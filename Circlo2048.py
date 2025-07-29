import string
import copy

## FUNCTIONS ##
def ret_indx(location,col,row,block)->int:
    indx=-1
    if location == "data":
        indx=data[block][col][row]
    if location == "accum_reader":
        indx=accum_block_reader[block][row]
    if location == "draw":
        indx=draw[block][col][row]
    if location == "accum":
        indx=accum[block][col][row]
    if location == "instruct":
        indx=instruct[block][row]
    if location == "randomizer":
        indx=randomizer[block][col][row]
    if location == "start":
        indx=start[col][row]
    if location == "arrow":
        indx=arrow[block][col][row]
    if location == "move":
        indx=movement[block][col]
    if (indx!=-1)&(indx!=0):
        return indx
    else:
        print("indexing error: " + location + " col: " + str(col) + " row: " + str(row) + " block: " + str(block))
        return -1

def log(location,col,row,block):
    global data,accum_block_reader
    if location == "data":
        data[block][col][row]=num
    if location == "accum_reader":
        accum_block_reader[block][row]=num
    if location == "draw":
        draw[block][col][row]=num
    if location == "accum":
        accum[block][col][row]=num
    if location == "instruct":
        instruct[block][row]=num
    if location == "randomizer":
        randomizer[block][col][row]=num
    if location == "start":
        start[col][row]=num
    if location == "arrow":
        arrow[block][col][row]=num
    if location == "move":
        movement[block][col]=num

def create_sptrigger(location,x,y,col,row,block)->string:
    global num
    num=num+1
    log(location,col,row,block)
    if location == "data":
        if col==0:
            if row==11:
                return "\nic 'ispo' "+str(x)+" "+str(y)+" 1\nsfx '5' 1 2 -1\n"+"< "+str(num)
    if location == "randomizer":
        if col==2:
            if row!=0:
                return "\nic 'ispo' " + str(x) + " " + str(y) + " 1 0 -1 True\ntrigger\nsfx 'house0' 1 3 -1\n" + "< " + str(num)
    if location == "none":
        return "\nic 'isp' " + str(player_x) + " " + str(player_y) + " 1 \nzoomFactor 2\ntrigger\nsfx 'none'\n" + "< " + str(num)
    return "\nic 'ispo' "+str(x)+" "+str(y)+" 1 0 -1 True\ntrigger\nsfx 'none'\n"+"< "+str(num)

def create_start_trigger(x,y,row):
    global num
    num=num+1
    log("start",3,row,0)
    if row==0:
        return "\nic 'isp' " + str(x) + " " + str(y) + " 1\ntrigger\nsfx 'house21' 1 2.5 -1\n" + "< " + str(num)
    if row==1:
        return "\nic 'isp' " + str(x) + " " + str(y) + " 1\ntrigger\nsfx 'house23' 1 2.5 -1\n" + "< " + str(num)

def create_circle(location,x,y,col,row,block)->string:
    global num,speed
    regen=599940
    off="off"
    delay=0
    num=num+1
    if location=="start":
        if col==5:
            delay=2
    if location=="randomizer":
        if col==5:
            delay=7
            if row==1:
                off="on"
        if col==4:
            delay=3
            if row==1:
                off="on"
        if (col==3)&(row==0):
            regen=3*speed
    if (location=="data")&(col==7)&(row!=0):
        delay=1
    if location=="move":
        delay=3
    if (location=="instruct"):
        delay=4
    if (location=="data")&(col==7)&(row==0):
        with open("2048py.txt", "a") as f:
            f.write("\ntmc "+str(x)+" "+str(y)+" 10 0 1 "+str(regen)+" "+str(1*speed)+"\nnoanim\n"+"on"+"\n"+"< "+str(num))
        num=num+1
    if (location=="data")&(col==0)&(row==0):
        delay=2
    if (location=="accum_reader")&(row==1):
        delay=1
    if (location=="accum")&(row==1)&(col==2):
        delay=2
    if (location=="accum")&(row==0)&(col==2):
        with open("2048py.txt", "a") as f:
            f.write("\ntmc "+str(x)+" "+str(y)+" 10 0 1 "+str(regen)+" "+str(1*speed)+"\nnoanim\n"+"on"+"\n"+"< "+str(num))
        num=num+1
    log(location,col,row,block)
    return "\ntmc "+str(x)+" "+str(y)+" 10 0 1 "+str(regen)+" "+str(delay*speed)+"\nnoanim\n"+off+"\n"+"< "+str(num)

def create_rectangle(x,y,width,height,col,row,block)->string:
    global num
    num=num+1
    log("draw",col,row,block)
    return "\ntmb "+str(x+(width/2))+" "+str(y+(height/2))+" "+str(width/2)+" "+str(height/2)+" 0 -1 0 -1 0 599940 0\nnoanim\noff\n"+"< "+str(num)

def create_arrow_rectangle(x,y,width,height,col,row,block)->string:
    global num
    off="off"
    num=num+1
    log("arrow",col,row,block)
    if (col==3):
        off="on"
    return "\ntmb "+str(x+(width/2))+" "+str(y+(height/2))+" "+str(width/2)+" "+str(height/2)+" 0 -1 0 -1 0 599940 0\nnoanim\n"+off+"\n"+"< "+str(num)

def create_start_rectangle(type,x,y,width,height,col,row,block)->string:
    global num
    num=num+1
    if type=="blue":
        return "\nb "+str(x+(width/2))+" "+str(y+(height/2))+" "+str(width/2)+" "+str(height/2)+" 0\n"+"< "+str(num)
    else:
        log("start",col,row,block)
        return "\ntmb "+str(x+(width/2))+" "+str(y+(height/2))+" "+str(width/2)+" "+str(height/2)+" 0 -1 0 -1 0 599940 0\nnoanim\noff\n"+"< "+str(num)

def create_connection(type,starting,ending):
    global num
    if starting==-1|ending==-1:
        print("connecting error: "+type+" starting: "+str(starting)+" ending: "+str(ending))
    num = num + 1
    with open("2048py.txt", "a") as f:
        f.write("\n> "+str(starting)+"\n> "+str(ending)+"\nspc '"+type+"'\n"+"< "+str(num))

def create_cell(location, x, y, col, row, block):
    with open("2048py.txt", "a") as f:
        f.write(create_sptrigger(location, x, y, col, row, block))
        if (location=="randomizer"):
            f.write(create_circle(location, x, y, col, row, block + 1))
        elif (location=="move"):
            if col==0:
                f.write(create_circle(location, x, y, col, row, block + 1))
        elif (location=="instruct"):
            f.write(create_circle(location, x, y, col, row, block + 4))
        elif (location=="accum"):
            f.write(create_circle(location, x, y, col, row, block + 8))
        elif (location=="start"):
            f.write(create_circle(location, x, y, col+4, row, block))
        else:
            f.write(create_circle(location, x, y, col, row, block + 16))

def create_draw_cell(j,k):
    with open("2048py.txt", "a") as f:
        block_x=draw_block_x+((k%4)*draw_spacing)
        block_y=draw_block_y+((k//4)*draw_spacing)
        if j==0:
            f.write(create_rectangle(block_x,block_y,5,90,j,0,k))
            f.write(create_rectangle(block_x+90,block_y+5,5,90,j,1,k))
            f.write(create_rectangle(block_x,block_y+90,90,5,j,2,k))
            f.write(create_rectangle(block_x+5,block_y,90,5,j,3,k))
        if j==1:
            f.write(create_rectangle(block_x+29.5,block_y+17.5,24,12,j,0,k))
            f.write(create_rectangle(block_x+53.5,block_y+17.5,12,36,j,1,k))
            f.write(create_rectangle(block_x+41.5,block_y+41.5,12,12,j,2,k))
            f.write(create_rectangle(block_x+29.5,block_y+41.5,12,36,j,3,k))
            f.write(create_rectangle(block_x+41.5,block_y+65.5,24,12,j,4,k))
        if j==2:
            f.write(create_rectangle(block_x+29.5,block_y+17.5,12,36,j,0,k))
            f.write(create_rectangle(block_x+41.5,block_y+41.5,12,12,j,1,k))
            f.write(create_rectangle(block_x+53.5,block_y+17.5,12,60,j,2,k))
        if j==3:
            f.write(create_rectangle(block_x+29.5,block_y+17.5,12,60,j,0,k))
            f.write(create_rectangle(block_x+41.5,block_y+17.5,12,12,j,1,k))
            f.write(create_rectangle(block_x+41.5,block_y+41.5,12,12,j,2,k))
            f.write(create_rectangle(block_x+41.5,block_y+65.5,12,12,j,3,k))
            f.write(create_rectangle(block_x+53.5,block_y+17.5,12,60,j,4,k))
        if j==4:
            f.write(create_rectangle(block_x+23,block_y+26.5,9.5,47.5,j,0,k))
            f.write(create_rectangle(block_x+43,block_y+26.5,9.5,47.5,j,1,k))
            f.write(create_rectangle(block_x+52.5,block_y+26.5,19,9.5,j,2,k))
            f.write(create_rectangle(block_x+52.5,block_y+45.5,9.5,9.5,j,3,k))
            f.write(create_rectangle(block_x+52.5,block_y+64.5,9.5,9.5,j,4,k))
            f.write(create_rectangle(block_x+62,block_y+45.5,9.5,28.5,j,5,k))
        if j==5:
            f.write(create_rectangle(block_x+14.5,block_y+26.5,19,9.5,j,0,k))
            f.write(create_rectangle(block_x+14.5,block_y+45.5,19,9.5,j,1,k))
            f.write(create_rectangle(block_x+14.5,block_y+64.5,19,9.5,j,2,k))
            f.write(create_rectangle(block_x+33.5,block_y+26.5,9.5,47.5,j,3,k))
            f.write(create_rectangle(block_x+52.5,block_y+26.5,19,9.5,j,4,k))
            f.write(create_rectangle(block_x+71.5,block_y+26.5,9.5,28.5,j,5,k))
            f.write(create_rectangle(block_x+62,block_y+45.5,9.5,9.5,j,6,k))
            f.write(create_rectangle(block_x+52.5,block_y+45.5,9.5,28.5,j,7,k))
            f.write(create_rectangle(block_x+62,block_y+64.5,19,9.5,j,8,k))
        if j==6:
            f.write(create_rectangle(block_x+14.5,block_y+26.5,9.5,47.5,j,0,k))
            f.write(create_rectangle(block_x+24,block_y+26.5,19,9.5,j,1,k))
            f.write(create_rectangle(block_x+24,block_y+45.5,9.5,9.5,j,2,k))
            f.write(create_rectangle(block_x+24,block_y+64.5,9.5,9.5,j,3,k))
            f.write(create_rectangle(block_x+33.5,block_y+45.5,9.5,28.5,j,4,k))
            f.write(create_rectangle(block_x+52.5,block_y+26.5,9.5,28.5,j,5,k))
            f.write(create_rectangle(block_x+62,block_y+45.5,9.5,9.5,j,6,k))
            f.write(create_rectangle(block_x+71.5,block_y+26.5,9.5,47.5,j,7,k))
        if j==7:
            f.write(create_rectangle(block_x+18,block_y+31,6.5,32.5,j,0,k))
            f.write(create_rectangle(block_x+31,block_y+31,19.5,6.5,j,1,k))
            f.write(create_rectangle(block_x+44,block_y+37.5,6.5,6.5,j,2,k))
            f.write(create_rectangle(block_x+31,block_y+44,19.5,6.5,j,3,k))
            f.write(create_rectangle(block_x+31,block_y+50.5,6.5,6.5,j,4,k))
            f.write(create_rectangle(block_x+31,block_y+57,19.5,6.5,j,5,k))
            f.write(create_rectangle(block_x+57,block_y+31,6.5,32.5,j,6,k))
            f.write(create_rectangle(block_x+63.5,block_y+31,6.5,6.5,j,7,k))
            f.write(create_rectangle(block_x+63.5,block_y+44,6.5,6.5,j,8,k))
            f.write(create_rectangle(block_x+63.5,block_y+57,6.5,6.5,j,9,k))
            f.write(create_rectangle(block_x+70,block_y+31,6.5,32.5,j,10,k))
        if j==8:
            f.write(create_rectangle(block_x+11.5,block_y+31,19.5,6.5,j,0,k))
            f.write(create_rectangle(block_x+24.5,block_y+37.5,6.5,6.5,j,1,k))
            f.write(create_rectangle(block_x+11.5,block_y+44,19.5,6.5,j,2,k))
            f.write(create_rectangle(block_x+11.5,block_y+50.5,6.5,6.5,j,3,k))
            f.write(create_rectangle(block_x+11.5,block_y+57,19.5,6.5,j,4,k))
            f.write(create_rectangle(block_x+38,block_y+31,19.5,6.5,j,5,k))
            f.write(create_rectangle(block_x+38,block_y+37.5,6.5,6.5,j,6,k))
            f.write(create_rectangle(block_x+38,block_y+44,19.5,6.5,j,7,k))
            f.write(create_rectangle(block_x+51,block_y+50.5,6.5,6.5,j,8,k))
            f.write(create_rectangle(block_x+38,block_y+57,19.5,6.5,j,9,k))
            f.write(create_rectangle(block_x+64,block_y+31,6.5,32.5,j,10,k))
            f.write(create_rectangle(block_x+70.5,block_y+31,13,6.5,j,11,k))
            f.write(create_rectangle(block_x+70.5,block_y+44,13,6.5,j,12,k))
            f.write(create_rectangle(block_x+70.5,block_y+57,13,6.5,j,13,k))
            f.write(create_rectangle(block_x+77,block_y+50.5,6.5,6.5,j,14,k))
        if j==9:
            f.write(create_rectangle(block_x+18,block_y+31,19.5,6.5,j,0,k))
            f.write(create_rectangle(block_x+18,block_y+37.5,6.5,6.5,j,1,k))
            f.write(create_rectangle(block_x+18,block_y+44,19.5,6.5,j,2,k))
            f.write(create_rectangle(block_x+31,block_y+50.5,6.5,6.5,j,3,k))
            f.write(create_rectangle(block_x+18,block_y+57,19.5,6.5,j,4,k))
            f.write(create_rectangle(block_x+44,block_y+31,6.5,32.5,j,5,k))
            f.write(create_rectangle(block_x+57,block_y+31,19.5,6.5,j,6,k))
            f.write(create_rectangle(block_x+70,block_y+37.5,6.5,6.5,j,7,k))
            f.write(create_rectangle(block_x+57,block_y+44,19.5,6.5,j,8,k))
            f.write(create_rectangle(block_x+57,block_y+50.5,6.5,6.5,j,9,k))
            f.write(create_rectangle(block_x+57,block_y+57,19.5,6.5,j,10,k))
        if j==10:
            f.write(create_rectangle(block_x+15,block_y+35,5,25,j,0,k))
            f.write(create_rectangle(block_x+25,block_y+35,5,25,j,1,k))
            f.write(create_rectangle(block_x+30,block_y+35,5,5,j,2,k))
            f.write(create_rectangle(block_x+30,block_y+55,5,5,j,3,k))
            f.write(create_rectangle(block_x+35,block_y+35,5,25,j,4,k))
            f.write(create_rectangle(block_x+45,block_y+35,15,5,j,5,k))
            f.write(create_rectangle(block_x+55,block_y+40,5,5,j,6,k))
            f.write(create_rectangle(block_x+45,block_y+45,15,5,j,7,k))
            f.write(create_rectangle(block_x+45,block_y+50,5,5,j,8,k))
            f.write(create_rectangle(block_x+45,block_y+55,15,5,j,9,k))
            f.write(create_rectangle(block_x+65,block_y+35,5,15,j,10,k))
            f.write(create_rectangle(block_x+70,block_y+45,5,5,j,11,k))
            f.write(create_rectangle(block_x+75,block_y+35,5,25,j,12,k))
        if j==11:
            f.write(create_rectangle(block_x+10,block_y+35,15,5,j,0,k))
            f.write(create_rectangle(block_x+20,block_y+40,5,5,j,1,k))
            f.write(create_rectangle(block_x+10,block_y+45,15,5,j,2,k))
            f.write(create_rectangle(block_x+10,block_y+50,5,5,j,3,k))
            f.write(create_rectangle(block_x+10,block_y+55,15,5,j,4,k))
            f.write(create_rectangle(block_x+30,block_y+35,5,25,j,5,k))
            f.write(create_rectangle(block_x+35,block_y+35,5,5,j,6,k))
            f.write(create_rectangle(block_x+35,block_y+55,5,5,j,7,k))
            f.write(create_rectangle(block_x+40,block_y+35,5,25,j,8,k))
            f.write(create_rectangle(block_x+50,block_y+35,5,15,j,9,k))
            f.write(create_rectangle(block_x+55,block_y+45,5,5,j,10,k))
            f.write(create_rectangle(block_x+60,block_y+35,5,25,j,11,k))
            f.write(create_rectangle(block_x+70,block_y+35,5,25,j,12,k))
            f.write(create_rectangle(block_x+75,block_y+35,5,5,j,13,k))
            f.write(create_rectangle(block_x+75,block_y+45,5,5,j,14,k))
            f.write(create_rectangle(block_x+75,block_y+55,5,5,j,15,k))
            f.write(create_rectangle(block_x+80,block_y+35,5,25,j,16,k))

def data_send_connect(col,row,block):
    self=ret_indx("data",col,row,block)
    self_circle=ret_indx("data",col,row,block+16)
    col_top=ret_indx("data",col,0,block)
    eq=ret_indx("data",7,row,block)
    zero_trigger=ret_indx("data",7,0,block)
    zero_circle=ret_indx("data",7,0,block+16)
    if col==1:
        transferblock=-1
    if col==2:
        transferblock=-4
    if col==3:
        transferblock=1
    if col==4:
        transferblock=4
    transfer=ret_indx("data",7,row,block+transferblock+16)
    create_connection("Reset",self,zero_circle)
    create_connection("Reset",self,transfer)
    create_connection("Deactivate",zero_trigger,self)
    create_connection("Reactivate",eq,self)
    create_connection("Reset",col_top,self_circle)

def accum_data_interface_connect(col,row,block):
    self=ret_indx("data",col,row,block)
    self_circle=ret_indx("data",col,row,block+16)
    col_top_circle=ret_indx("data",col,0,block+16)
    zero_eq=ret_indx("data",7,row,block)
    zero_top=ret_indx("data",7,0,block)
    accum_link=ret_indx("accum_reader",-1,col-5,block)
    create_connection("Deactivate",zero_top,self)
    create_connection("Reactivate",zero_eq,self)
    create_connection("Reset",accum_link,self_circle)

def zero_connect(col,row,block):
    self=ret_indx("data",col,row,block)
    zero=ret_indx("data",0,row,block)
    inc=ret_indx("data",8,row,block)
    acc1_top=ret_indx("data",5,0,block)
    acc2_top=ret_indx("data",6,0,block)
    create_connection("Reactivate",self,zero)
    create_connection("Reactivate",self,inc)
    create_connection("Deactivate",self,acc1_top)
    create_connection("Deactivate",self,acc2_top)

def inc_connect(col,row,block):
    self=ret_indx("data",col,row,block)
    self_circle=ret_indx("data",col,row,block+16)
    zero_top=ret_indx("data",7,0,block)
    zero_rop_circle=ret_indx("data",7,0,block+16)
    inc_top=ret_indx("data",col,0,block)
    if row!=11:
        zero_low_cirle=ret_indx("data",col-1,row+1,block+16)
        create_connection("Reset",self,zero_low_cirle)
    create_connection("Reset",inc_top,self_circle)
    create_connection("Reset",self,zero_rop_circle)
    create_connection("Deactivate",zero_top,self)

def random_0_connect(col,row):
    self=ret_indx("randomizer",col,row,0)
    self_circle=ret_indx("randomizer",col,row,1)
    eq_2=ret_indx("randomizer",2,row,0)
    top_0=ret_indx("randomizer",0,0,0)
    top_1=ret_indx("randomizer",1,0,0)
    link=ret_indx("data",7,1,(row+15))
    create_connection("Reset",eq_2,self_circle)
    create_connection("Reactivate",top_0,self)
    create_connection("Deactivate",top_1,self)
    create_connection("Reset",self,link)

def random_1_connect(col,row):
    self=ret_indx("randomizer",col,row,0)
    self_circle = ret_indx("randomizer", col, row, 1)
    eq_2 = ret_indx("randomizer", 2, row, 0)
    top_0=ret_indx("randomizer",0,0,0)
    top_1=ret_indx("randomizer",1,0,0)
    link=ret_indx("data",7,2,row+15)
    create_connection("Reset", eq_2, self_circle)
    create_connection("Reactivate",top_1,self)
    create_connection("Deactivate",top_0,self)
    create_connection("Reset",self,link)

def random_2_connect(col,row):
    self=ret_indx("randomizer",col,row,0)
    top_2_circle=ret_indx("randomizer",2,0,1)
    zero=ret_indx("data",7,0,row-1)
    create_connection("Reset",self,top_2_circle)
    create_connection("Reactivate",zero,self)
    for i in range(11):
        create_connection("Deactivate",ret_indx("data",7,i+1,row-1),self)

def random_3_connect(col,row):
    self=ret_indx("randomizer",col,row,0)
    self_circle=ret_indx("randomizer",col,row,1)
    top_3=ret_indx("randomizer",3,0,0)
    eq_2_circle=ret_indx("randomizer",2,(((row-1)*7)%16)+1,1)
    eq_4=ret_indx("randomizer",4,row,0)
    if row!=16:
        low_4=ret_indx("randomizer",4,row+1,0)
    else:
        low_4=ret_indx("randomizer",4,1,0)
    create_connection("Deactivate",low_4,self)
    create_connection("Reactivate",eq_4,self)
    create_connection("Reset",self,eq_2_circle)
    create_connection("Reset",top_3,self_circle)
    create_connection("Deactivate",start_trigger,self)

def random_4_connect(col,row):
    self=ret_indx("randomizer",col,row,0)
    next=(row)%16+1
    prev=(row+14)%16+1
    next_circle=ret_indx("randomizer",col,next,1)
    prev_circle=ret_indx("randomizer",col,prev,1)
    create_connection("Reset",self,next_circle)
    create_connection("Destroy",self,prev_circle)

def random_5_connect(col,row):
    if row<11:
        self=ret_indx("randomizer",col,row,0)
        next=(row)%10+1
        prev=(row+8)%10+1
        next_circle=ret_indx("randomizer",col,next,1)
        prev_circle=ret_indx("randomizer",col,prev,1)
        create_connection("Reset",self,next_circle)
        create_connection("Destroy",self,prev_circle)

def draw_connect(col,row,block):
    self=ret_indx("data",col,row,block)
    self_circle=ret_indx("data",col,row,block+16)
    col_top=ret_indx("data",col,0,block)
    zero_top=ret_indx("data",7,0,block)
    create_connection("Deactivate",zero_top,self)
    create_connection("Reset",col_top,self_circle)
    for i in range(draw_lens[row]):
        create_connection("NowIf",self,ret_indx("draw",row,i,block))
        create_connection("Destroy",ret_indx("data",col,0,block),ret_indx("draw",row,i,block))
    for j in range(draw_lens[0]):
        create_connection("NowIf", self, ret_indx("draw", 0, j, block))

def start_connect_0(col,row):
    self=ret_indx("start",col,row,0)
    self_circle=ret_indx("start",col+4,row,0)
    eq_1=ret_indx("start",col+1,row,0)
    eq_2=ret_indx("start",col+2,row,0)
    eq_1_down=ret_indx("start",col+1,(row+1)%4,0)
    right_trigger=ret_indx("start",3,1,0)
    create_connection("Reactivate",eq_1,self)
    create_connection("Deactivate",eq_2,self)
    create_connection("Deactivate",eq_1_down,self)
    create_connection("Reset",right_trigger,self_circle)
    if (row==1)|(row==3):
        create_connection("Reset",self,ret_indx("instruct",-1,0,row+4))
    else:
        create_connection("Reset",self,ret_indx("instruct",-1,0,6-row))
    if row>0:
        create_connection("Deactivate",start_trigger,self)

def start_connect_1(col,row):
    self=ret_indx("start",col,row,0)
    self_circle=ret_indx("start",col+4,row,0)
    eq_2=ret_indx("start",2,row,0)
    eq_2_up=ret_indx("start",col+1,(row-1)%4,0)
    right_rect=ret_indx("start",3,2,0)
    left_rect=ret_indx("start",3,3,0)
    create_connection("Destroy",self,right_rect)
    create_connection("Destroy",self,left_rect)
    create_connection("Deactivate",eq_2,self)
    create_connection("Reactivate",self,eq_2)
    create_connection("Reactivate",eq_2_up,self)
    create_connection("Deactivate",self,eq_2_up)
    create_connection("Reset",eq_2_up,self_circle)
    if row>0:
        create_connection("Deactivate",start_trigger,self)
    for i in range(7):
        create_connection("NowIf",self,ret_indx("arrow",(row+3)%4,i,0))
        create_connection("Destroy",self,ret_indx("arrow",(row+2)%4,i,0))

def start_connect_2(col,row):
    self=ret_indx("start",col,row,0)
    self_circle=ret_indx("start",col+4,row,0)
    left_trigger=ret_indx("start",3,0,0)
    create_connection("Reset",left_trigger,self_circle)
    if row>0:
        create_connection("Deactivate",start_trigger,self)

def accum_0_connect(row,col,block):
    if accum[block][col][row]!=-1:
        if block<4:
            offset=2
            accum1=ret_indx("accum_reader",-1,0,28-(4*(row-1))+block)
        if block>=4:
            offset=3
            accum1=ret_indx("accum_reader",-1,0,20-row+(4*(block-4)))
        self=ret_indx("accum",col,row,block)
        self_circle=ret_indx("accum",col,row,block+8)
        if row==1:
            create_connection("Reset",ret_indx("instruct",-1,0,offset),self_circle)
            create_connection("Reset",ret_indx("instruct",-1,3,offset),self_circle)
            create_connection("Reset",ret_indx("instruct",-1,5,offset),self_circle)
            create_connection("Reset",ret_indx("instruct",-1,6,offset),self_circle)
        if row==2:
            create_connection("Reset",ret_indx("instruct",-1,2,offset-2),self_circle)
            create_connection("Reset",ret_indx("instruct",-1,8,offset-2),self_circle)
            create_connection("Reset",ret_indx("instruct",-1,10,offset-2),self_circle)
            create_connection("Reset",ret_indx("instruct",-1,1,offset),self_circle)
            create_connection("Reset",ret_indx("instruct",-1,4,offset),self_circle)
            create_connection("Reset",ret_indx("instruct",-1,7,offset),self_circle)
            create_connection("Reset",ret_indx("instruct",-1,9,offset),self_circle)
        if row==3:
            create_connection("Reset",ret_indx("instruct",-1,2,offset),self_circle)
            create_connection("Reset",ret_indx("instruct",-1,8,offset),self_circle)
            create_connection("Reset",ret_indx("instruct",-1,10,offset),self_circle)
            create_connection("Reset",ret_indx("instruct",-1,1,offset-2),self_circle)
            create_connection("Reset",ret_indx("instruct",-1,4,offset-2),self_circle)
            create_connection("Reset",ret_indx("instruct",-1,7,offset-2),self_circle)
            create_connection("Reset",ret_indx("instruct",-1,9,offset-2),self_circle)
        if row==4:
            create_connection("Reset",ret_indx("instruct",-1,0,offset-2),self_circle)
            create_connection("Reset",ret_indx("instruct",-1,3,offset-2),self_circle)
            create_connection("Reset",ret_indx("instruct",-1,5,offset-2),self_circle)
            create_connection("Reset",ret_indx("instruct",-1,6,offset-2),self_circle)
        create_connection("Reset",self,accum1)
        create_connection("Reactivate",self,ret_indx("accum",3,row,block))

def accum_1_connect(row,col,block):
    if accum[block][col][row]!=-1:
        if block<4:
            offset=2
            accum1=ret_indx("accum_reader",-1,1,28-(4*(row-1))+block)
        if block>=4:
            offset=3
            accum1=ret_indx("accum_reader",-1,1,20-row+(4*(block-4)))
        self=ret_indx("accum",col,row,block)
        self_circle=ret_indx("accum",col,row,block+8)
        if row==1:
            create_connection("Reset",ret_indx("instruct",-1,2,offset-2),self_circle)
            create_connection("Reset",ret_indx("instruct",-1,8,offset-2),self_circle)
            create_connection("Reset",ret_indx("instruct",-1,10,offset-2),self_circle)
        if row==2:
            create_connection("Reset",ret_indx("instruct",-1,0,offset),self_circle)
            create_connection("Reset",ret_indx("instruct",-1,3,offset),self_circle)
            create_connection("Reset",ret_indx("instruct",-1,5,offset),self_circle)
            create_connection("Reset",ret_indx("instruct",-1,6,offset),self_circle)
            create_connection("Reset",ret_indx("instruct",-1,1,offset-2),self_circle)
            create_connection("Reset",ret_indx("instruct",-1,4,offset-2),self_circle)
            create_connection("Reset",ret_indx("instruct",-1,7,offset-2),self_circle)
            create_connection("Reset",ret_indx("instruct",-1,9,offset-2),self_circle)
        if row==3:
            create_connection("Reset",ret_indx("instruct",-1,0,offset-2),self_circle)
            create_connection("Reset",ret_indx("instruct",-1,3,offset-2),self_circle)
            create_connection("Reset",ret_indx("instruct",-1,5,offset-2),self_circle)
            create_connection("Reset",ret_indx("instruct",-1,6,offset-2),self_circle)
            create_connection("Reset",ret_indx("instruct",-1,1,offset),self_circle)
            create_connection("Reset",ret_indx("instruct",-1,4,offset),self_circle)
            create_connection("Reset",ret_indx("instruct",-1,7,offset),self_circle)
            create_connection("Reset",ret_indx("instruct",-1,9,offset),self_circle)
        if row==4:
            create_connection("Reset",ret_indx("instruct",-1,2,offset),self_circle)
            create_connection("Reset",ret_indx("instruct",-1,8,offset),self_circle)
            create_connection("Reset",ret_indx("instruct",-1,10,offset),self_circle)
        create_connection("Reset",self,accum1)
        create_connection("Reactivate",self,ret_indx("accum",4,row,block))
        create_connection("Reactivate",self,ret_indx("accum",5,row,block))
        create_connection("Reactivate",self,ret_indx("accum",6,row,block))

def accum_2_connect(row,col,block):
    self=ret_indx("accum",col,row,block)
    self_circle=ret_indx("accum",col,row,block+8)
    col_top=ret_indx("accum",col,0,block)
    if row==0:
        for i in range(2):
            for j in range(1,11):
                create_connection("Reset",ret_indx("instruct",-1,j,(2*i)+(block//4)),self_circle)
        for i in range(4):
            create_connection("Reset",ret_indx("instruct",-1,0,i),self_circle)
    elif row==1:
        create_connection("Reset",col_top,self_circle)
        create_connection("Deactivate", col_top, self)
        create_connection("Reset", self, ret_indx("accum",5,0,block+8))
        create_connection("Reset", self, ret_indx("accum",6,0,block+8))
        if block<4:
            for i in range(4):
                create_connection("Reactivate",ret_indx("data",5,row-1,(i*4)+block),self)
                create_connection("Deactivate",ret_indx("data",6,row-1,(i*4)+block),self)
        else:
            for i in range(4):
                create_connection("Reactivate",ret_indx("data",5,row-1,((block-4)*4)+i),self)
                create_connection("Deactivate",ret_indx("data",6,row-1,((block-4)*4)+i),self)
    else:
        create_connection("Deactivate",col_top,self)
        create_connection("Reset", self, ret_indx("accum",3,0,block+8))
        create_connection("Reset", self, ret_indx("accum",4,0,block+8))
        if block<4:
            for i in range(4):
                create_connection("Reactivate",ret_indx("data",5,row-1,(i*4)+block),self)
                create_connection("Reset",ret_indx("data",6,row-1,(i*4)+block),self_circle)
        else:
            for i in range(4):
                create_connection("Reactivate",ret_indx("data",5,row-1,((block-4)*4)+i),self)
                create_connection("Reset",ret_indx("data",6,row-1,((block-4)*4)+i),self_circle)

def accum_3_4_connect(row,col,block):
    self=ret_indx("accum",col,row,block)
    self_circle=ret_indx("accum",col,row,block+8)
    if block<4:
        offset=2
        link=16+(4*(4-row))+block
    else:
        offset=3
        link=16+(4-row)+(4*(block-4))
    if row==0:
        for i in range(2):
            create_connection("Deactivate",ret_indx("instruct",-1,0,offset-(2*i)),self)
            create_connection("Reactivate",ret_indx("instruct",-1,6,offset-(2*i)),self)
            create_connection("Deactivate",ret_indx("instruct",-1,9,offset-(2*i)),self)
    else:
        create_connection("Deactivate",ret_indx("accum",2,0,block),self)
        create_connection("Reset",ret_indx("accum",col,0,block),self_circle)
        if col==3:
            if data[link][7][0]!=0:
                create_connection("Reset",self,ret_indx("data",8,0,link))
        if col==4:
            if data[link][8][0]!=0:
                create_connection("Reset",self,ret_indx("data",7,0,link))

def accum_5_6_connect(row,col,block):
    self=ret_indx("accum",col,row,block)
    self_circle=ret_indx("accum",col,row,block+8)
    if block<4:
        offset=2
        link=16+(4*(4-row))+block
        if row==0:
            create_connection("Reactivate",ret_indx("instruct",-1,0,offset-(2*(6-col))),self)
            create_connection("Deactivate",ret_indx("instruct",-1,6,offset-(2*(6-col))),self)
            create_connection("Deactivate",ret_indx("instruct",-1,0,offset-(2*(col-5))),self)
            create_connection("Reactivate",ret_indx("instruct",-1,9,offset-(2*(6-col))),self)
    else:
        offset=1
        link=16+(4-row)+(4*(block-4))
        if row==0:
            create_connection("Reactivate",ret_indx("instruct",-1,0,offset+(2*(6-col))),self)
            create_connection("Deactivate",ret_indx("instruct",-1,6,offset+(2*(6-col))),self)
            create_connection("Deactivate",ret_indx("instruct",-1,0,offset+(2*(col-5))),self)
            create_connection("Reactivate",ret_indx("instruct",-1,9,offset+(2*(6-col))),self)
    if row!=0:
        create_connection("Deactivate",ret_indx("accum",2,0,block),self)
        create_connection("Reset",ret_indx("accum",col,0,block),self_circle)
        if col==5:
            if block<4:
                if data[link][2][0]!=0:
                    create_connection("Reset",self,ret_indx("data",2,0,link))
            else:
                if data[link][3][0]!=0:
                    create_connection("Reset",self,ret_indx("data",3,0,link))
        if col==6:
            if block<4:
                if data[link][4][0]!=0:
                    create_connection("Reset",self,ret_indx("data",4,0,link))
            else:
                if data[link][1][0]!=0:
                    create_connection("Reset",self,ret_indx("data",1,0,link))

## INITIALIZATION ##
num=0
speed=2
spacing=44
draw_spacing=95
start_trigger=8
data_block_x=-100
data_block_y=360
draw_block_x=1500-(2*draw_spacing)
draw_block_y=3000
accum_x=data_block_x+(40*spacing)
accum_y=data_block_y+(3*spacing)
randomizer_x=accum_x
randomizer_y=accum_y+(31*spacing)
start_x=randomizer_x+(7*spacing)
start_y=randomizer_y
player_x=start_x+(6*spacing)
player_y=start_y+(1.5*spacing)
movement_x=randomizer_x+(4*spacing)
movement_y=randomizer_y
data=[] ## [block][col][row] ## triggers blocks 0-15 circles blocks 16-31
accum_block_reader=[]
accum_block=[[-1,0,0,0,0,-1,-1,-1,-1,-1,-1,-1,-1],[-1,0,0,0,0,-1,-1,-1,-1,-1,-1,-1,-1],[0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,-1,-1,-1,-1,-1,-1,-1,-1],[0,0,0,0,0,-1,-1,-1,-1,-1,-1,-1,-1],[0,0,0,0,0,-1,-1,-1,-1,-1,-1,-1,-1],[0,0,0,0,0,-1,-1,-1,-1,-1,-1,-1,-1]]
accum=[]
draw=[]
instruct=[]
draw_lens=[4,5,3,5,6,9,8,11,15,11,13,17]
randomizer=[]
start=[]
arrow=[]
arrows_x=[-17.5,-22.5,-27.5,-32.5,-27.5,-22.5,-17.5]
arrows_y=[-15,-10,-5,0,5,10,15]
arrows_width=[10,10,10,70,10,10,10]
arrows_height=[5,5,5,5,5,5,5]
check_x=[-25,-20,-15,-10,-5,0,5,10,15,20,25,30]
check_y=[15,15,20,25,20,10,0,-10,-20,-25,-30,-30]
check_width=5
check_height=[5,10,10,10,10,15,15,15,15,10,10,5]
x_x=[-25,-20,-15,-10,-5,0,5,10,15,20,25,-25,-20,-15,-10,-5,5,10,15,20,25]
x_y=[-25,-20,-15,-10,-5,0,5,10,15,20,25,25,20,15,10,5,-5,-10,-15,-20,-25]
x_width=5
x_height=5
arrow_1_x=1202.5
arrow_2_x=1792.5
arrow_y=3332.5
movement=[]

for k in range(32):
    block = []
    accum_block_reader.append([0,0])
    for i in range(9):
        row = []
        for j in range(12):
            row.append(0);
        block.append(row)
    data.append(block)
for k in range(16):
    block = []
    for j in range(12):
        row = []
        for i in range(draw_lens[j]):
            row.append(0)
        block.append(row)
    draw.append(block)
for k in range(16):
    accum.append(copy.deepcopy(accum_block))
for k in range(8):
    instruct_block = []
    for j in range(11):
        instruct_block.append(0)
    instruct.append(instruct_block)
for k in range(2):
    randomizer_block=[]
    for i in range(6):
        randomizer_row=[]
        for j in range(17):
            randomizer_row.append(0)
        randomizer_block.append(randomizer_row)
    randomizer.append(randomizer_block)
    for z in range(4,6):
        randomizer[k][z][0]=-1
    for z in range(11,17):
        randomizer[k][5][z]=-1
for k in range(8):
    start_block=[]
    for j in range(5):
        start_block.append(0)
    start.append(start_block)
for k in range(2):
    block=[]
    for j in range(4):
        col=[]
        for i in range(21):
            col.append(0)
        block.append(col)
    arrow.append(block)
for k in range(2):
    block=[]
    for j in range(2):
        block.append(0)
    movement.append(block)

## HEADER ##
f=open("2048py.txt","w")
with open("2048py.txt","a") as f:
    f.write("/\n/ circloO level\n/ Made with circloO Level Editor\ntotalCircles 10 1\n/ EDITOR_TOOL 0\n/ EDITOR_VIEW 1500 1500 0.20\n/ EDT 55555\n/ _SAVE_TIME_1751919988000_END\nlevelscriptVersion 9\nCOLORS 35\ngrav 0 270\ngs "+str(player_x)+" "+str(player_y)+" 0\ny "+str(player_x)+" "+str(player_y)+" 1 1 1\nbullet\n< 0\n")
    with open("GUI.txt","r") as f2:
        f.write(f2.read())
        num=120

## PLAYER AREA CREATION ##
for i in range (2):
    with open("2048py.txt", "a") as f:
        f.write(create_start_trigger(player_x-59+(118*i),player_y,i))
        f.write(create_start_rectangle("green",player_x-53+(86*i),player_y-35,20,70,3,2+i,0))
with open("2048py.txt", "a") as f:
    f.write(create_start_rectangle("blue",player_x-89,player_y-55,178,20,-1,-1,-1))
    f.write(create_start_rectangle("blue",player_x-89,player_y-35,20,70,-1,-1,-1))
    f.write(create_start_rectangle("blue",player_x-89,player_y+35,178,20,-1,-1,-1))
    f.write(create_start_rectangle("blue",player_x+69,player_y-35,20,70,-1,-1,-1))
for i in range(3):
    for j in range(4):
        create_cell("start",start_x+(spacing*i),start_y+(spacing*j),i,j,0)

## ARROW CREATION ##
for i in range(4):
    with open("2048py.txt", "a") as f:
        temp_x=arrows_x
        temp_y=arrows_y
        temp_width=arrows_width
        temp_height=arrows_height
        if (i%2==1):
            temp_y=arrows_x
            temp_x=arrows_y
            temp_width=arrows_height
            temp_height=arrows_width
        for j in range(7):
            if (i//2==1):
                temp_x[j]=temp_x[j]*-1
                if (i%2==0):
                    temp_x[j]=temp_x[j]-temp_width[j]+5
            f.write(create_arrow_rectangle(arrow_1_x+temp_x[j],arrow_y+temp_y[j],temp_width[j],temp_height[j],i,j,0))
for j in range(12):
    with open("2048py.txt", "a") as f:
        f.write(create_arrow_rectangle(arrow_2_x+check_x[j],arrow_y+check_y[j],check_width,check_height[j],0,j,1))
for j in range(21):
    with open("2048py.txt", "a") as f:
        f.write(create_arrow_rectangle(arrow_2_x+x_x[j],arrow_y+x_y[j],x_width,x_height,1,j,1))

## DATA BLOCK CREATION ##
for i in range(9):
    for j in range(12):
        for k in range(16):
            if (((k//4!=0)|(i!=2))&((k//4!=3)|(i!=4))&((k%4!=0)|(i!=1))&((k%4!=3)|(i!=3))):
                create_cell("data",data_block_x+(spacing*i)+((k%4)*spacing*10),data_block_y+(spacing*j)+((k//4)*spacing*13),i,j,k)

## ACCUM BLOCK READER CREATION ##
for i in range(16):
    for j in range(2):
        create_cell("accum_reader",data_block_x+(spacing*(5+j))+((i%4)*spacing*10),data_block_y+(-spacing)+((i//4)*spacing*13),-1,j,i)

## DRAW BLOCK CREATION ##
for k in range(16):
    for j in range(12):
        create_draw_cell(j,k)

## ACCUM BLOCK CREATION ##
for i in range(7):
    for j in range(13):
        for k in range(8):
            if accum[k][i][j]!=-1:
                create_cell("accum",accum_x+(spacing*i)+((k%4)*spacing*8),accum_y+(spacing*j)+((k//4)*spacing*15),i,j,k)

## INSTRUCT CREATION ##
for i in range(11):
    for k in range(4):
        create_cell("instruct",accum_x+(spacing*i)+((k%2)*spacing*16),accum_y-(spacing*3)+((k//2)*spacing),-1,i,k)

## RANDOMIZER CREATION ##
for i in range(6):
    for j in range(17):
        if (randomizer[0][i][j]!=-1):
            create_cell("randomizer",randomizer_x+(spacing*i),randomizer_y+(spacing*j),i,j,0)

## MOVEMENT DETECTION CREATION ##
for i in range(2):
    create_cell("move",movement_x,movement_y,i,-1,0)

## DATA BLOCK LINKING ##
for i in range(1,5):
    for k in range(16):
        if (((k//4!=0)|(i!=2))&((k//4!=3)|(i!=4))&((k%4!=0)|(i!=1))&((k%4!=3)|(i!=3))):
            for j in range(1,12):
                data_send_connect(i,j,k)
            create_connection("Deactivate",ret_indx("data",i,0,k),ret_indx("move",0,0,0))
            create_connection("Reactivate",ret_indx("data",i,0,k),ret_indx("move",1,0,0))
for i in range(5,7):
  for k in range(16):
      for j in range(1,12):
          accum_data_interface_connect(i,j,k)
      create_connection("Reset",ret_indx("accum_reader",-1,i-5,k),ret_indx("data",i,0,k+16))
      create_connection("Reactivate",ret_indx("data",7,0,k),ret_indx("data",i,0,k))
for i in range(7,8):
    for k in range(16):
        for j in range(1,12):
            zero_connect(i,j,k)
for i in range(8,9):
    for k in range(16):
        for j in range(1,12):
            inc_connect(i,j,k)
        create_connection("Deactivate",ret_indx("data",i,0,k),ret_indx("move",0,0,0))
        create_connection("Reactivate",ret_indx("data",i,0,k),ret_indx("move",1,0,0))
for i in range(0,1):
    for k in range(16):
        for j in range(1,12):
            draw_connect(i,j,k)
        for j in range(draw_lens[0]):
            create_connection("Destroy",ret_indx("data",i,0,k),ret_indx("draw",0,j,k))
        create_connection("Reset",ret_indx("randomizer",2,0,0),ret_indx("data",0,0,k+16))
        create_connection("Reset",ret_indx("move",1,0,0),ret_indx("data",0,0,k+16))

## ACCUM BLOCK LINKING ##
for k in range(8):
    for j in range(7):
        for i in range(13):
            if accum[k][j][i]!=-1:
                if j==0:
                    accum_0_connect(i,j,k)
                if j==1:
                    accum_1_connect(i,j,k)
                if j==2:
                    accum_2_connect(i,j,k)
                if (j==3)|(j==4):
                    accum_3_4_connect(i,j,k)
                if (j==5)|(j==6):
                    accum_5_6_connect(i,j,k)
for k in range(4):
    for j in range(10):
        create_connection("Reset",ret_indx("instruct",-1,j,k),ret_indx("instruct",-1,j+1,k+4))
    create_connection("Reset",ret_indx("instruct",-1,10,k),ret_indx("move",0,0,1))

## RANDOMIZER BLOCK LINKING ##
for k in range(1):
    for i in range(6):
        for j in range(1,17):
            if (randomizer[0][i][j]!=-1):
                if i==0:
                    random_0_connect(i,j)
                if i==1:
                    random_1_connect(i,j)
                if i==2:
                    random_2_connect(i,j)
                if i==3:
                    random_3_connect(i,j)
                if i==4:
                    random_4_connect(i,j)
                if i==5:
                    random_5_connect(i,j)
    create_connection("Reset",ret_indx("randomizer",5,1,0),ret_indx("randomizer",1,0,1))
    create_connection("Reset",ret_indx("randomizer",5,2,0),ret_indx("randomizer",0,0,1))
    create_connection("Off",ret_indx("randomizer",2,0,0),ret_indx("randomizer",3,0,1))
    create_connection("Reset",ret_indx("move",0,0,0),ret_indx("randomizer",2,0,1))
    create_connection("Reset",ret_indx("move",1,0,0),ret_indx("randomizer",3,0,1))

## START LINKING ##
for i in range(3):
    for j in range(4):
        if i==0:
            start_connect_0(i,j)
        if i==1:
            start_connect_1(i,j)
        if i==2:
            start_connect_2(i,j)
for i in range(2):
    left_rect=ret_indx("start",3,2,0)
    right_rect=ret_indx("start",3,3,0)
    self=ret_indx("start",3,i,0)
    create_connection("NowIf",self,left_rect)
    create_connection("NowIf",self,right_rect)
create_connection("Destroy",ret_indx("randomizer",2,0,0),left_rect)
create_connection("Destroy",ret_indx("randomizer",2,0,0),right_rect)
for i in range(12):
    right_trigger=ret_indx("start",3,1,0)
    create_connection("Destroy",right_trigger,ret_indx("arrow",0,i,1))
    create_connection("NowIf",ret_indx("randomizer",2,0,0),ret_indx("arrow",0,i,1))
for i in range(21):
    right_trigger=ret_indx("start",3,1,0)
    create_connection("Destroy",ret_indx("randomizer",2,0,0),ret_indx("arrow",1,i,1))
    create_connection("NowIf",right_trigger,ret_indx("arrow",1,i,1))
create_connection("Reactivate",ret_indx("start",3,1,0),ret_indx("move",0,0,0))
create_connection("Deactivate",ret_indx("start",3,1,0),ret_indx("move",1,0,0))

num=num+1
with open("2048py.txt", "a") as f:
    f.write("\nic 'isp' "+str(player_x+59)+" "+str(player_y)+" 1\ntrigger\n"+"< "+str(num))
num=num+1
with open("2048py.txt", "a") as f:
    f.write("\ntmc "+str(randomizer_x+(spacing*3))+" "+str(randomizer_y)+" 10 0 1 599940 "+str(90)+"\nnoanim\noff\n"+"< "+str(num))
create_connection("Reset",num-1,num)
create_connection("Deactivate",ret_indx("start",3,1,0),num-2)