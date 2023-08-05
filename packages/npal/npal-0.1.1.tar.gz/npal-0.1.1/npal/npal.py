import os
import os.path
import datetime as dt
import shutil
import time
from string import Template
from hashlib import scrypt
from base64 import urlsafe_b64encode
from cryptography.fernet import Fernet, InvalidToken
from getpass import getpass
from selenium.webdriver import ChromeOptions
from selenium.common.exceptions import NoSuchWindowException
import helium as he
import pandas as pd
from pandas.api.types import CategoricalDtype
import numpy as np
import xlrd
import gspread


class Npal():
    file = '.credential'
    Days = ['MON', 'TUES', 'WED', 'THUR', 'FRI', 'SAT', 'SUN']
    Day_type = CategoricalDtype(categories=Days, ordered=True)


    @staticmethod
    def generate_cipher(userkey):
        salt = b'\xf9(&\xb3\xc9\xd1X\xd4\x94\xe6a$f\x88\xef\x8a'  # urandom(16)
        key = scrypt(userkey.encode(), salt=salt, n=16384, r=8, p=1, dklen=32)
        cipher = Fernet(urlsafe_b64encode(key))
        return cipher


    @classmethod
    def read_credential(cls, passphrase):
        if os.path.isfile(cls.file):
            with open(cls.file, 'rb') as f:
                npnet_id, password = f.read().split(b':', 1)

            cipher = Npal.generate_cipher(passphrase)
            try:
                password = cipher.decrypt(password)
                del cipher
                return (npnet_id.decode(), password.decode())
            except:
                del cipher
                return (None, None)
        else:
            return (None, None)


    @classmethod
    def write_credential(cls, passphrase):
        npnet_id = input('Enter NPnet ID: ')
        password = getpass('Enter password: ')
        cipher = Npal.generate_cipher(passphrase)
        password = cipher.encrypt(password.encode()).decode()
        with open(cls.file, 'w') as f: 
            f.write(f'{npnet_id}:{password}')
        return npnet_id, password


    @staticmethod
    def chrome_download_complete(driver):
        '''
        Monitor download completion
        '''
        if not driver.current_url.startswith("chrome://downloads"):
            driver.get("chrome://downloads/")

        driver.execute_script("""
            var items = document.querySelector('downloads-manager')
                .shadowRoot.getElementById('downloadsList').items;
            if (items.every(e => e.state === "COMPLETE"))
                return items.map(e => e.fileUrl || e.file_url);
            """
        )
        return True


    @staticmethod
    def chrome_prefs(download_dir):
        '''
        Change default download directory and behaviour
        '''
        options = ChromeOptions()
        options.add_experimental_option(
            'prefs', {
                'download.default_directory': download_dir,
                'download.prompt_for_download': False,
                'download.directory_upgrade': True
            }
        )
        return options


    @staticmethod
    def move_file(old_fullpathname, dest_dir, filename, overwrite=False):
        '''
        Move old_fullpathname to dest_dir/filename
        If overwrite is True and dirname(old_fullpathname)/filename exists, 
        the existing file will be overwritten. Otherwise the existing file
        will be renamed using timestamp.
        '''
        old_basename = os.path.dirname(old_fullpathname)
        #old_filename, old_ext = os.path.splitext(os.path.basename(old_fullpathname))
        new_filename, new_ext = os.path.splitext(filename)

        srcname = os.path.join(old_basename, new_filename+new_ext)
        dstname = os.path.join(dest_dir,     new_filename+new_ext)

        # If a file with the same name exists,
        if os.path.isfile(srcname):
            if overwrite == False:
            # Rename the file using current time
                now = str(dt.datetime.now())[:19]
                for c in ' :-': now = now.replace(c, '')
                srcname2 = os.path.join(old_basename, new_filename+'_'+now+new_ext)
                os.rename(srcname, srcname2)
            else:
                os.remove(srcname)

        # old_fullpathname -> srcname -> dstname
        os.rename(old_fullpathname, srcname)
        if srcname != dstname:
            shutil.move(srcname, dstname)


    @staticmethod
    def start_Npal(dest_dir, options=None):
        url = 'https://npalcs.np.edu.sg/psp/staff/EMPLOYEE/SA/h/?tab=DEFAULT&cmd=login&errorCode=106&languageCd=ENG'
        driver = he.start_chrome(url, options=Npal.chrome_prefs(dest_dir))
        if not os.path.isfile('.credential'):
            passphrase = getpass('Enter your secret passphrase: ')
            npnetid, password = Npal.write_credential(passphrase)
            del passphrase
        else:
            npnetid, password = Npal.read_credential(getpass('Enter your secret passphrase: '))
        Npal.write(npnetid, into='User Id')
        Npal.write(password, into='Password')
        Npal.click('Sign in')
        del password
        return driver


    @staticmethod
    def query_report(driver, query, dest_dir, filename, *args):
        '''
        Query NPAL report which does not require parameters
        '''
        t = Template("window.open('https://npalcs.np.edu.sg/psc/staff_5/EMPLOYEE/SA/q/?ICAction=ICQryNameExcelURL=PUBLIC.${query}')")
        script = t.substitute(query=query)
        try:
            driver.execute_script(script)
            driver.switch_to.window(driver.window_handles[1])
            Npal.wait_until(Npal.chrome_download_complete)
        except NoSuchWindowException:
            # The download has completed too quickly
            Npal.sleep(3)
            pass
        finally:
            old_filename = max([dest_dir + f for f in os.listdir(dest_dir)],key=os.path.getctime)
            if old_filename:
                Npal.move_file(old_filename, dest_dir, filename)
                print(f'Report is at {dest_dir}/{filename}')
                return True
            else:
                print(f'Failed to download')


    @staticmethod
    def query_report2(driver, query):
        t = Template("window.open('https://npalcs.np.edu.sg/psc/staff_5/EMPLOYEE/SA/q/?ICAction=ICQryNameExcelURL=PUBLIC.${query}')")
        script = t.substitute(query=query)
        driver.execute_script(script)
        driver.switch_to.window(driver.window_handles[1])


    @staticmethod
    def click(text):
        he.click(text)


    @staticmethod
    def write(text, into=None):
        he.write(text, into=into)


    @staticmethod
    def download(driver, dest_dir, element, seconds):
        Npal.click(element)
        Npal.wait_until(Npal.chrome_download_complete)
        Npal.sleep(seconds)
        
        downloaded_file = max([dest_dir + f for f in os.listdir(dest_dir)],
                              key=os.path.getctime
                             )
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        return downloaded_file


    @staticmethod
    def wait_until(condition_fn, timeout_secs=10, interval_secs=0.5):
        he.wait_until(condition_fn, timeout_secs=timeout_secs, interval_secs=interval_secs)


    @staticmethod
    def close_browser():
        he.kill_browser()


    @staticmethod
    def sleep(seconds):
        time.sleep(seconds)


    @staticmethod
    def parse_ASRQ407(infile, effdate=None, header=0, usecols=None):
        '''
        Parse ARQ407 excel file and filter rows with 'Eff Date' >= effdata
        @effdate is a string with 'yyyy-mm-dd' format
        Return a DataFrame object
        '''
        df = pd.read_excel(
            xlrd.open_workbook(infile, logfile=open(os.devnull, 'w')),
            header=header,
            usecols=usecols,
            converters={
                'Module ID': lambda x: str(x) if x else '',
                'Catalog'  : lambda x: x.strip(),
                'Rqrmnt'   : lambda x: str(x) if x else '',
                'Rq Group' : lambda x: str(x) if x else '',
                'Sublevel' : lambda x: str(x) if x else '',
                'Eff Date' : pd.to_datetime,
            }
        )

        if effdate: df=df[df['Eff Date'] >= effdate]

        # Remove time from 'Eff Date' and then make it a string type
        df['Eff Date'] = pd.to_datetime(
            df['Eff Date'], format='%yyyy-%mm-%dd'
        ).astype(str)

        return df 


    @staticmethod
    def df2gs(
        df,
        gid,
        sn='Sheet1',
        gcred='gdrive.json',
    ):
        '''
        Transfer a dataframe object to a Google Sheet
        @df - Dataframe
        @gid - Google Sheet ID
        @sn - Sheet name
        @gcred - Crentiantial in JSON to access Google Drive
        
        Note: 
        1. All date and time field must be first converted to string
        2. All NaN values must be converted to ''
        '''
        df = df.fillna('')  # Replace NaN to ''
        
        gsurl = 'https://docs.google.com/spreadsheets/d/'
        gc = gspread.service_account(filename=gcred)
        wb = gc.open_by_key(gid)
        ws_list = [ws.title for ws in wb.worksheets()]
        if sn in ws_list:
            ws = wb.worksheet(sn)
            ws.clear()
        else:
            ws = wb.add_worksheet(
            title=sn,
            rows=df.shape[0],
            cols=df.shape[1]
        )

        ws.update(
            [df.columns.values.tolist()] + df.values.tolist()
        )
        print()
        print(f'Generated output to {gsurl}{gid}')


    @staticmethod
    def parse_NSRQ966(infile, acadprogs=None, header=0, usecols=None):
        '''
        Parse NSRQ966 excel file
        @acadprogs - filter list of rows with the following acad programs
        @header - position of header row
        @usecols - columns to be used to retrieve the data
        '''
        df = pd.read_excel(
            xlrd.open_workbook(infile, logfile=open(os.devnull, 'w')),
            header=header,
            converters={
                'Module ID':   lambda x: str(x) if x else '',
                'Catalog Nbr': lambda x: x.strip(),
                'Day':         lambda x: str(x)[0:3] if x != "" and len(x) < 5 else x,
                'Instr Id':    lambda x: str(x),
                'Start Time':  lambda x: str(x)[0:5] if len(x) == 5 else '',
                'End Time':    lambda x: str(x)[0:5] if len(x) == 5 else '',
            }
        )

        # Filter required acad programs
        if acadprogs: df = df[df['Acad Prog'].isin(acadprogs)]

        # Compute Hour and Load Start/End Times and Meeting Pattern fields
        df['Hour'] = (
            pd.to_datetime(df['End Time']) - pd.to_datetime(df['Start Time'])
        ).dt.total_seconds() / 3600.0
        df['Load'] = df['Hour']
        df.loc[df['Meeting Pattern'].isin(['ODD','EVEN']),'Load'] = df['Load']*0.5

        # Split and explode rows with multiple days inside Day field
        df['Day'] = df['Day'].str.split()
        df = df.explode('Day').reset_index(drop=True)
        
        # Categorical type for 'Day' field
        df['Day'] = df['Day'].astype(Npal.Day_type)

        if usecols: df=df[usecols]
        return df


if __name__ == '__main__':
    Npal.write_credential(getpass('Enter your secret passphrase: '))
    npnetid, password = Npal.read_credential(getpass('Enter your secret passphrase: '))
    print(f'npnet_id={npnetid}\npassword={password}')
