"""
----------------------------------------
  - Based on pysigfox.py by Hecko

  - Developed by Mencho: 08/02/2017

  - Last Update: 09/10/2017
----------------------------------------
- Classes
        -sigfox
- Methods
    - device_types_list
    - device_list_id
    - device_all_messages
    - device_n_messages
    - device_all_messages_time

"""
import socket
import json 
import ast
import time
import datetime
import requests
import requests.packages.urllib3

## Request timeout
TIMEOUT = 30

class sigfox:
    def __init__(self, login, password):
        if not login or not password:
            raise Exception("Login/Pass is needed it")
        self.login = login
        self.password = password
        self.api_url = 'https://backend.sigfox.com/api/'

    def login_test(self):
        """Test sigfox Backend login"""
        url = self.api_url + 'devicetypes'
        try:
            req = requests.get(url, auth=requests.auth.HTTPBasicAuth(self.login, self.password))
            req.raise_for_status()
            print "Login Complete\n"
        except requests.exceptions.RequestException as err:
            print err
        except socket.error as err:
            print err


    def device_types_list(self):
        """Return device type list

            Keyword arguments:
            None          

            Return arguments:
            List with all the device types 
        """
        out = []

        url = self.api_url + 'devicetypes'
        try:
            req = requests.get(url, auth=requests.auth.HTTPBasicAuth(self.login, self.password))
            req.raise_for_status()
            for device in json.loads(req.text)['data']:
                out.append(device['id'])
            out = ast.literal_eval(json.dumps(out))
        except requests.exceptions.RequestException  as err:
            print err
        except socket.error as err:
            print err
        return out       


    def device_list_id(self, device_type_id=0):
        """Return device list

           Keyword arguments:
           device_type_id          -- device types 
    
           Return arguments:
           List with all the PIDs 
        """
        device_type_ids = []
        out = []
        
        if device_type_id != 0:
            device_type_ids.append(device_type_id)
        else:
            device_type_ids = self.device_types_list()

        for device_type_id in device_type_ids:
            url = self.api_url + 'devicetypes/' + device_type_id + '/devices?limit=100'
            try:
                req = requests.get(url, auth=requests.auth.HTTPBasicAuth(self.login, self.password))
                req.raise_for_status()
                results = req.json()
                for result in results['data']:
                    out.append(result['id'])
                out = ast.literal_eval(json.dumps(out))
                next_url = (results['paging']).get('next')
                while next_url:
                    url = next_url
                    try:
                        req = requests.get(url, 
                                           auth=requests.auth.HTTPBasicAuth(self.login, 
                                                                            self.password), 
                                           timeout=TIMEOUT)
                        req.raise_for_status()
                        results = req.json()
                        for result in results['data']:
                            out.append(result['id'])
                        out = ast.literal_eval(json.dumps(out))    
                        next_url = (results['paging']).get('next')
                        time.sleep(1)
                    except requests.exceptions.RequestException as err:
                        print err
                    except socket.error as err:
                        print err
            except requests.exceptions.RequestException as err:
                print err
            except socket.error as err:
                print err
        return out


    def device_all_messages(self, device_id):
        """Return a list with all sigfox messages
           
           Keyword arguments:
           device_id          -- device PID
    
           Return arguments:
           List with all the messages 
        """
        out = []

        url = self.api_url + 'devices/' + str(device_id) + '/messages?limit=100' 
        try:
            req = requests.get(url, 
                               auth=requests.auth.HTTPBasicAuth(self.login, self.password), 
                               timeout=TIMEOUT)
            req.raise_for_status()
            results = req.json()
            results = ast.literal_eval(json.dumps(results))
            for result in results['data']:
                out.append([result['device'],
                            time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(result['time'])), 
                            result['snr'], 
                            result['linkQuality'], 
                            result['data']])
            next_url = (results['paging']).get('next')
            while next_url:
                url = next_url
                try:
                    req = requests.get(url, 
                                       auth=requests.auth.HTTPBasicAuth(self.login, self.password), 
                                       timeout=TIMEOUT)
                    req.raise_for_status()
                    results = req.json()
                    results = ast.literal_eval(json.dumps(results))
                    for result in results['data']:
                        out.append([result['device'],
                                    time.strftime('%Y-%m-%d %H:%M:%S', 
                                                  time.localtime(result['time'])), 
                                    result['snr'], 
                                    result['linkQuality'], 
                                    result['data']])
                    next_url = (results['paging']).get('next')
                    time.sleep(1)
                except requests.exceptions.RequestException as err:
                    print err
                except socket.error as err:
                    print err
        except requests.exceptions.RequestException as err:
            print err
        except socket.error as err:
            print err
        return out


    def device_n_messages(self, device_id, n_messages):
        """Return a list up to N sigfox messages    

           Keyword arguments:
           device_id          -- device PID
           n_messages         -- Max number of messages
    
           Return arguments:
           List with n messages 
        """
        out = []
        num_frames = 0

        if n_messages <= 100:
            url = self.api_url + 'devices/' + str(device_id) + '/messages?limit=' + str(n_messages) 
        else:
            url = self.api_url + 'devices/' + str(device_id) + '/messages?limit=100' 
        try:
            req = requests.get(url, 
                               auth=requests.auth.HTTPBasicAuth(self.login, self.password), 
                               timeout=TIMEOUT)
            req.raise_for_status()
            results = req.json()
            results = ast.literal_eval(json.dumps(results))
            for result in results['data']:
                out.append([result['device'], 
                            time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(result['time'])), 
                            result['snr'], 
                            result['linkQuality'], 
                            result['data']])
                num_frames = num_frames + 1
            next_url = (results['paging']).get('next')          
            n_messages = n_messages - num_frames
            while (next_url != None) and (num_frames <= n_messages):
                url = next_url
                try:
                    req = requests.get(url, 
                                       auth=requests.auth.HTTPBasicAuth(self.login, self.password), 
                                       timeout=TIMEOUT)
                    req.raise_for_status()
                    results = req.json()
                    results = ast.literal_eval(json.dumps(results))
                    for result in results['data']:
                        out.append([result['device'], 
                                    time.strftime('%Y-%m-%d %H:%M:%S',\
                                    time.localtime(result['time'])), 
                                    result['snr'], 
                                    result['linkQuality'], 
                                    result['data']])
                        num_frames = num_frames + 1
                    next_url = (results['paging']).get('next')
                except requests.exceptions.RequestException as err:
                    print err
                except socket.error as err:
                    print err
                    time.sleep(60)
        except requests.exceptions.RequestException as err:
            print err
        except socket.error as err:
            print err
        return out


    def device_all_messages_time(self, device_id, since_time, upto_time):
        """Return a list with all messages between since_time and upto_time

           Keyword arguments:
           device_id          -- device PID
           n_messages         -- Max number of messages
           since_time         -- Start time (epoch format)
           upto_time          -- Finish time (epoch format)
    
           Return arguments:
           List with n messages between since_time and upto_time
        """
        out = []

        try:
            since_epoch = int(time.mktime(time.strptime(since_time, '%Y-%m-%d')))
            upto_epoch = int(time.mktime(time.strptime(upto_time, '%Y-%m-%d')))
        except ValueError:
            print "Error with the date conversion"
        if since_epoch > upto_epoch:
            print 'upto_time should be bigger than since_time'
            exit()
        url = self.api_url + 'devices/' + str(device_id) + '/messages?since=' + \
              str(since_epoch) + '&before=' + str(upto_epoch)
        try:
            req = requests.get(url, 
                               auth=requests.auth.HTTPBasicAuth(self.login, self.password), 
                               timeout=TIMEOUT)
            req.raise_for_status()
            results = req.json()
            results = ast.literal_eval(json.dumps(results))
            for result in results['data']:
                out.append([result['device'],
                            time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(result['time'])), 
                            result['snr'], 
                            result['linkQuality'], 
                            result['data']])
            next_url = (results['paging']).get('next')
            while next_url:
                url = next_url
                try:
                    req = requests.get(url, 
                                       auth=requests.auth.HTTPBasicAuth(self.login, self.password), 
                                       timeout=TIMEOUT)
                    req.raise_for_status()
                    results = req.json()
                    results = ast.literal_eval(json.dumps(results))
                    for result in results['data']:
                        out.append([result['device'],
                                    time.strftime('%Y-%m-%d %H:%M:%S', \
                                    time.localtime(result['time'])), 
                                    result['snr'], 
                                    result['linkQuality'], 
                                    result['data']])        
                    next_url = (results['paging']).get('next')
                except requests.exceptions.RequestException as err:
                    print err
                except socket.error as err:
                    print err
        except requests.exceptions.RequestException as err:
            print err
        except socket.error as err:
            print err
        return out