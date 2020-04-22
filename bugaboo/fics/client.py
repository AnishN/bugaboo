from telnetlib import Telnet

class InvalidUsernameError(Exception):
    def __init__(self):
        super().__init__("Username must be 3-17 alphabetical-only characters")

class InvalidPasswordError(Exception):
    def __init__(self):
        super().__init__("Wrong password")

class FICS(object):

    def __init__(self):
        self.connection = Telnet()
        self.username = None
        self.password = None
        
        """
        Available commands
        abort          accept       addlist      adjourn        alias    
        allobservers   assess       backward     bell           best     
        boards         bsetup       bugwho       cbest                   
        clearmessages  convert_bcf  convert_elo  convert_uscf            
        copygame       crank        cshout       date           decline  
        draw           examine      finger       flag           flip     
        fmessage       follow       forward      games          gnotify  
        goboard        handles      hbest        help           history  
        hrank          inchannel    index        info           it       
        jkill          jsave        kibitz       limits         llogons  
        logons         mailhelp     mailmess     mailmoves               
        mailoldmoves   mailsource   mailstored   match                   
        messages       mexamine     moretime     moves          news     
        next           observe      oldmoves     open           password 
        pause          pending      pfollow      play           pobserve 
        promote        pstat        qtell        quit           rank     
        refresh        resign       resume       revert         say      
        seek           servers      set          shout          showlist 
        simabort       simallabort  simadjourn   simalladjourn           
        simgames       simmatch     simnext      simobserve              
        simopen        simpass      simprev      smoves                  
        smposition     sought       sposition    statistics     stored   
        style          sublist      switch       takeback       tell     
        time           unalias      unexamine    unobserve      unpause  
        unseek         uptime       variables    whisper        who      
        withdraw       xkibitz      xtell        xwhisper       znotify  
        AUTHORS
        -------

        Created: 23 July 1998 Friar
        Last Modified: 28 February 2008 mhill
        """
        
        #self.connection.read_until(b":")
        #self.connection.close()

    def connect(self, username, password):
        host = "freechess.org"
        port = 5000
        u_bytes = username.encode("utf-8")
        p_bytes = password.encode("utf-8")

        if not self.is_valid_username(username):
            self.disconnect()
            raise InvalidUsernameError()
        self.connection.open(host, port)
        self.connection.read_until(b"login: ")
        self.connection.write(u_bytes + b"\r\n")
        self.connection.read_until(b"password:")
        out = self.connection.write(p_bytes + b"\r\n")
        index, match, out = self.connection.expect([b"login:", b"fics%"])
        if match.group(0) == b"login:":
            self.disconnect()
            raise InvalidPasswordError()
        else:
            pass
        self.username = username
        self.password = password
    
    def is_valid_username(self, username):
        u_len = len(username)
        if u_len < 3 or u_len > 17:
            return False
        elif not username.isalpha():
            return False
        return True

    def disconnect(self):
        self.connection.write(b"quit")
        self.connection.close()
        self.connection = None

    """
    def abort_game(self):
        pass

    def accept_abort_game(self):
        pass
    """