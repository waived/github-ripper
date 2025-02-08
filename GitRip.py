import requests
import os
import re
import sys
import git
from bs4 import BeautifulSoup

#set colors
w = '\033[1m\033[37m' #white
r = '\033[1m\033[31m' #red
g = '\033[1m\033[32m' #green
b = '\033[1m\033[34m' #blue
c = '\033[1m\033[36m' #cyan

def main():
    #refresh env
    os.system("clear")
    
    #display banner
    print(f'''{c}
          .aMMMMP dMP dMMMMMMP dMP dMP dMP dMP dMMMMb
         dMP     amr    dMP   dMP dMP dMP dMP dMP dMP
        dMP MMP dMP    dMP   dMMMMMP dMP dMP dMMMMK 
       dMP dMP dMP    dMP   dMP dMP dMP aMP dMP aMF
       VMMMP" dMP    dMP   dMP dMP  VMMMP" dMMMMP"{b}

     dMMMMb  dMP dMMMMb  dMMMMb  dMMMMMP dMMMMb
    dMP dMP amr dMP dMP dMP dMP dMP     dMP dMP
   dMMMMK  dMP dMMMMP" dMMMMP" dMMMP   dMMMMK 
  dMP AMF dMP dMP     dMP     dMP     dMP AMF
 dMP dMP dMP dMP     dMP     dMMMMMP dMP dMP{w}
''')
    
    #capture user input
    try:
        profile = input(f' {w}Github User (ex "Waived"):{r} ')
        
        path = input(f' {w}Path to download (ex- /tmp/):{r} ')
        
        if not os.path.isdir(path):
            sys.exit(f'\r\n {r}Invalid path! Exiting...\r\n')
            
        input(f'{w}\r\n Ready? Strike <ENTER> to rip and <CTRL+C> to end...\r\n')
    except KeyboardInterrupt:
        sys.exit()
    except Exception as ex:
        sys.exit(f'\r\n {r}Error: {ex}\r\n')

    #begin ripping repositories
    
    flag = True
    
    page = 0
    
    repositories = []
    
    print(f' {b}[{c}~{b}] {w}Scraping page/s. This may take some time...\r\n')
    
    while flag:
        page +=1
        
        try:
            #setup sequential url
            url = f'https://github.com/{profile}?tab=repositories&page={page}'
            
            #get page content
            response = requests.get(url)
            
            #end of page detected
            if "doesn’t have any public repositories yet" in response.text:
                flag = False
                continue
            
            print(f' {w}---> Extracting hyperlinks: {g}{url}')
            
            if not response.status_code == 200:
                #either blocked or no more pages left
                flag = False
                continue
            else:
                #parse using BeautifulSoup
                soup = BeautifulSoup(response.text, 'html.parser')
                
                #extract all links
                src_links = soup.find_all(src=True)
                
                #filter links that start with "/waived" and remove everything before "/graphs/"
                filtered_links = [link['src'].split('/graphs', 1)[0] for link in src_links if link['src'].startswith('/waived') and '/graphs' in link['src']]
                
                #format extracted links
                for link in filtered_links:
                    new_link = f'https://github.com{link}.git'
                    #append to main link-list
                    repositories.append(new_link)
                    
        except Exception as ex:
            print(ex)

    #clone each repository
    print(f'\r\n {b}[{c}!{b}] {w}Now cloning each repository!\r\n')
    
    for repository in repositories:
        try:
            print(f' {w}---> Downloading: {g}{repository}')
            
            #extract repository name
            match = re.search(r"/waived/(.*?)\.git", repository)
            
            folder_name = match.group(1)
            
            #setup path to clone into
            repo_path = os.path.join(path, folder_name)
            
            #make folder
            os.mkdir(repo_path)
            
            #clone into folder
            git.Repo.clone_from(repository, repo_path)
        except Exception as ex:
            print(ex)

    print(f'\r\n {w}Complete!\r\n')

if __name__ == '__main__':
    main()
