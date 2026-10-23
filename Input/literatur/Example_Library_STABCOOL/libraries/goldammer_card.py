### Author: f_scheiber
### For this class the newest Goldammer drivers need to be installed on your device.
### Get them at https://goldammer.de/multichoice-usb-basic/ "Systemtreiber"

import warnings
from time import sleep, time
import hashlib
import libraries.lib.MAIv2Win32.maiv2 as m

import numpy as np

from device_interface import *

# Cards can be uniquely identified by their card hash. This is done to differentiate multiple cards plugged into the same system.
# Goldammer MultiChoice USB basic G0V-1034-0:       30555830
# Geitmann Siconn USB basic G0S-1034-0 "System 1":  18767066
# Geitmann Siconn USB basic G0S-1034-0 "System 2":  60898255

known_cards = {30555830: 'Goldammer MultiChoice USB basic G0V-1034-0',
               18767066: 'Geitmann Siconn USB basic G0S-1034-0 \"System 1\"',
               60898255: 'Geitmann Siconn USB basic G0S-1034-0 \"System 2\"'
               }

def hash_from_id(card_id:int):
    if (card_id+1) > m.GetNumberOfDevices():
        raise ValueError('You tried to access a device that isn\'t connected. Choose a lower device id.')
    #generating unique hash value from device specific information
    manufacturer = decode_bytes(m.GetManufacture_Name(card_id))
    sn = decode_bytes(m.GetSerialNumber(card_id))
    dop = decode_bytes(m.GetCustomer_DateOfPurchase(card_id))
    hashstring = manufacturer + sn + dop
    hsh = int(str(int(hashlib.md5(hashstring.encode('utf-8')).hexdigest(), 16))[:8])
    return hsh

def id_from_hash(card_hash:int):
    id_list = []
    #identifying device by its hash
    for id in range(m.GetNumberOfDevices()):
        if card_hash == hash_from_id(id):
            id_list.append(id)
    if len(id_list) == 1:
        return id_list[0]
    elif len(id_list) > 1:
        raise ValueError('Multiple fitting cards are connected and cannot be distinguished by hash!')
    elif len(id_list) == 0:
        return -1
    else:
        raise NotImplementedError('How did you even get here? Shush!')

def connected_cards():
    card_num = m.GetNumberOfDevices()
    cards = {}
    for card_ID in range(card_num):
        card_hash = hash_from_id(card_ID)
        if card_hash in known_cards.keys():
            card_name = known_cards[card_hash]
        else:
            card_name = f'Unknown card {decode_bytes(m.GetSerialNumber(card_ID))}'
        cards[card_hash] = card_name
    return cards


class AD_Channel:
    def __init__(self, channel_ID:int, **kwargs):
        if type(channel_ID) is int:
            self.channel_ID = channel_ID
        else:
            self.channel_ID = int(channel_ID)
        self.name = str(channel_ID)
        self.highpass = False
        self.gain = m.enumGain.Disabled

        self.IEPE = False
        self.b_gain = False
        self.DC_coupling = False
        self.differential = False

        self.polarity = m.enumBipolar.BIPOLAR

        self.update_properties(**kwargs)

    def update_properties(self, **kwargs):
        self.__dict__.update(kwargs)

class GoldammerCard:
    def __init__(self, card_hash:int = None, card_id:int = None, sample_rate:int = 200000):
        # try to find a measurement card in the following order:
        # 1. by hash (if set. known card)
        if type(card_hash) == int:
            self.cardID = id_from_hash(card_hash)
        # 2. by id (if set. might be different if multiple cards are connected)
        elif type(card_id) == int:
            self.cardID = card_id
        # 3. by whichever is the first card available
        else:
            self.cardID = m.GetFirstDevice()
            if self.cardID == -1000:
                raise OSError("No Measurement card is connected.")

        ## AD properties
        # read card properties
        self.card_number = decode_bytes(m.GetSerialNumber(self.cardID))
        self.num_AD_channels = m.GetADChannels(self.cardID)
        self.AD_ChannelList = [AD_Channel(num) for num in range(self.num_AD_channels)]

        self.max_AD_sample_rate = self.set_max_sample_rate()
        self.max_AD_sample_width = m.GetADSampleWidth(self.cardID)

        self.sample_rate = self.set_sample_rate(sample_rate)

        self.AD_data_type = np.float64
        if m.GetADSampleWidth(cardID=self.cardID) == 16:
            self.AD_data_type = np.float16
        elif m.GetADSampleWidth(cardID=self.cardID) == 32:
            self.AD_data_type = np.float32

        self.oversampling = m.enumOversampling.DISABLED

        # take so much of what is in FIFO memory
        #self.memory_fraction = 0.9

        self.recording = False
        self.reset_card()


    def set_max_sample_rate(self):
        if 'G0V-1034-0' in self.card_number:
            return int(192*1e3)
        elif 'G0S-1034-0' in self.card_number:
            return int(float(m.GetADSampleRate(self.cardID)) / float(self.num_AD_channels))
        else:
            raise ValueError('Unknown measurement card. Max AD sample rate could not be set')

    def set_sample_rate(self, sample_rate):
        try:
            if not type(sample_rate) == int:
                sample_rate = int(sample_rate)
        except TypeError as err:
            print(f'AD sample rate is not a number: {err}')

        if 'G0V-1034-0' in self.card_number:
            possible_sampling_rates = (np.asarray([8, 16, 24, 32, 44.1, 48, 96, 192]) * 1e3).astype(int)
            if sample_rate in possible_sampling_rates:
                sr = sample_rate
                print(f'AD sample rate set to {sr}')
            elif sample_rate > np.max(possible_sampling_rates):
                sr = np.max(possible_sampling_rates)
                print(f"Chosen AD sample rate is too high. AD sample rate set to card max: {sr}")
            else:
                sr = min([s for s in possible_sampling_rates if s>sample_rate])
                print(f'Chosen AD sample rate not supported by card. AD sample rate instead set to {sr}')

        elif 'G0S-1034-0' in self.card_number:
            if sample_rate > self.max_AD_sample_rate:
                sr = self.max_AD_sample_rate
                print(f"Chosen AD sample rate is too high. AD sample rate set to card max: {sr}")
            else:
                sr = self.sample_rate

        else:
            print(f"Unknown measurement card. AD sample rate was set to {sample_rate}")
            sr = sample_rate
        return sr

    def setup_channel(self, channelID:int):
        if self.num_AD_channels <= channelID:
            raise ValueError(f'Number of AD_Channel too high: {channelID}')

        print(f'Setting up channel {channelID} for measurement:')
        channel = self.AD_ChannelList[channelID]

        if m.AD_GetIEPEType(self.cardID) != 1 and channel.IEPE:
            raise ValueError(f'Channel {channelID} demands IEPE, however measurement Card does not support it!')

        # "AD_SetIEPE"

        if channel.DC_coupling:
            if channel.differential:
                mode = m.enumIEPEMode.DC_Diff_IEPE_off
                print('- DC coupling \n- differential measurement \n- IEPE off')
            else:
                mode = m.enumIEPEMode.DC_SE_IEPE_off
                print('- DC coupling \n- single-ended measurement \n- IEPE off')
        else:
            if channel.IEPE:
                mode = m.enumIEPEMode.AC_SE_IEPE_on
                print('- AC coupling \n- single-ended measurement \n- IEPE on')
            else:
                mode = m.enumIEPEMode.AC_SE_IEPE_off
                print('- AC coupling \n- single-ended measurement \n- IEPE off')

        if channel.b_gain:
            print('- +20dB gain applied')
            bg = 1
        else:
            bg = 0
        m.AD_SetIEPE(cardID=self.cardID,
                     channelID=channelID,
                     nIEPEMode=mode,
                     bGain=bg)

        # AD_Audio_SetHPFilter

        if 'G0V-1034-0' in self.card_number:
            if channel.highpass:
                hpf = 1
            else:
                hpf = 0
            m.AD_Audio_SetHPFilter(cardID=self.cardID,
                                   channelID=channelID,
                                   bFilterOn=hpf)

        print(f'Setup of channel {channelID} complete.')

    def reset_card(self):
        if self.recording:
            self.stop_measuring()
        m.ResetDevice(self.cardID)
        m.ClearAllChannelLists(self.cardID)

    def start_measuring(self, channel_IDs, sample_rate=None, over_sampling = m.enumOversampling.DISABLED, IEPE_settling_time:float = 10.0):
        if sample_rate is not None and sample_rate != self.sample_rate:
            self.sample_rate = self.set_sample_rate(sample_rate)
        self.reset_card()
        self.recording = True
        for cID in channel_IDs:
            channel = self.AD_ChannelList[cID]
            self.setup_channel(cID)
            m.AD_AddChannelToList(cardID=self.cardID,
                                  channelID=cID,
                                  oversamplingMode=over_sampling,
                                  gainFactor=channel.gain,
                                  polarity=channel.polarity)
        if m.AD_GetChannelListSize(self.cardID) > 0:
            m.AD_SetFrequency(self.cardID, self.sample_rate)
            m.ConfigMeasure(self.cardID)
            if any([channel.IEPE for channel in [self.AD_ChannelList[cID] for cID in channel_IDs]]):
                print('Waiting for IEPE channels to settle...')
                sleep(IEPE_settling_time)
            m.AD_StartMeasure(self.cardID)
            print('Measurement started!')
            m.SetLEDs(self.cardID, True, False, False)
        else:
            print('No channel selected! Measurement was not started.')

    def stop_measuring(self):
        m.AD_StopMeasure(self.cardID)
        print('Measurement stopped!')
        m.SetLEDs(self.cardID, False, True, False)
        self.recording = False

    def fetch_block(self, blocksize:int = 1e3, timing = False):
        if timing:
            t1 = time()
        available_values = m.AD_GetNumberOfValues(self.cardID)
        #print(f'Available values = {available_values}')
        if available_values < blocksize:
            request_interval = max(float(blocksize) / float(self.sample_rate), 0.001)
            while available_values <= blocksize:
                sleep(request_interval)
                available_values = m.AD_GetNumberOfValues(self.cardID)
                #print(f'Available values = {available_values}')

        dat = [m.AD_ReadData(self.cardID, c, blocksize).astype(self.AD_data_type).T for c in
               range(m.AD_GetChannelListSize(self.cardID))]
        #print('Fetching Data')
        if timing:
            dt = time() - t1
            print(f'time per fetch loop: {dt}')
        return np.asarray(dat).T

    def collect_data(self, n:int, blocksize:int = 1e3, ignore_first:int = 0):
        n_tot = n+ignore_first
        if type(n_tot) != int:
            n_tot = int(n_tot)
        arr = np.zeros((n_tot, m.AD_GetChannelListSize(self.cardID)), dtype=self.AD_data_type)
        calls = int(np.ceil(n_tot / blocksize))
        for call in range(calls):
            #print(f'\nCall {call}')
            idx_min = int(call * blocksize)
            idx_max = idx_min + blocksize
            if m.AD_GetStreamPipeLevel(self.cardID) >= 10.0:
                warnings.warn(f'Stream pipe level at {m.AD_GetStreamPipeLevel(self.cardID)} while calling block {call+1}! Consider increasing blocksize to speed up data transfer!')
            if idx_max <= n_tot:
                arr[idx_min:idx_max, :] = self.fetch_block(blocksize)
            else:
                arr[idx_min:idx_max, :] = self.fetch_block(blocksize)[0:n_tot - idx_min, :]
        return arr[ignore_first:,:]