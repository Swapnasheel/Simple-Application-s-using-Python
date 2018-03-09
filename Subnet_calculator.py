'''

Simple Subnet Calculator!
Gives you number of hosts avaliable in the subnet along with other network node addresses

Author: Swapnasheel Sonkamble
Usage: python Subnet_calculator.py 

Can add:
    - Argparse

'''


import random
import sys



def convert_to_binary(octet):

    return_octet = []

    for octet_index in range(0, len(octet)):

        binary_octet = bin(int(octet[octet_index])).split("b")[1]

        if len(binary_octet) < 8:
            binary_octet_padded = binary_octet.zfill(8)
            return_octet.append(binary_octet_padded)
        else:
            return_octet.append(binary_octet)

    return return_octet



def convert_to_decimal(whole_octet):

    return_octet = []

    for each_octet in whole_octet:
        return_octet.append(str(int(each_octet, 2)))

    return return_octet



def get_random_ip_address(network_ip, broadcast_ip):

    try:
        while True:

            generate = raw_input("Do you wish to generate random IP address? y/n.  ")

            if generate.lower() == 'y' or generate.lower() == 'yes':
                generated_ip = []

                for broadcast_index, broadcast_octet in enumerate(broadcast_ip):
                    for network_index, network_octet in enumerate(network_ip):

                        if broadcast_index == network_index:
                            if broadcast_octet == network_octet:
                                generated_ip.append(broadcast_octet)
                            else:
                                generated_ip.append(str(random.randint(int(network_octet), int(broadcast_octet))))
                new_ip_add = ".".join(generated_ip)

                print "\nRandomly generated IP address is : %s" %new_ip_add
                print '\n'
                continue

            else:
                print "Bye!!"
                break

    except KeyboardInterrupt:
        print "\nForce Exiting!!! \n"
        print "BYE!!!"



def Main():

    try:
        print "\n"
         
        while True:
            ip_add = raw_input("Enter an IP address: ").split('.')

            '''
            Check for a valid IP address
            Make sure the IP address has:
                1. 4 Octets
                2. Maximum value of 255 in each octet
                3. Check for Link local IP address
                4. Not loopback or belonging to class E
            '''

            if ( len(ip_add) == 4) and (1 <= int(ip_add[0]) <= 255) and int(ip_add[0])!=0 and (int(ip_add[0])!=169) or int(ip_add[1])!=254 and int(ip_add[0]) != 224 and (1 <= int(ip_add) <= 255) and (1 <= int(ip_add[2]) <= 255) and (1 <= int(ip_add[3]) <= 255):
                break

            else:
                print "Ip address invalid!!! Please retry!!"
                continue

        masks = [255, 254, 252, 248, 240, 224, 192, 128, 0]

        while True:
            subnet_mask = raw_input("Enter the subnet mask: ").split('.')

            # Subnet mask checking as per above checks

            if ( len(subnet_mask) == 4 and int(subnet_mask[0]) == 255 and (int(subnet_mask[1]) in masks) and (int(subnet_mask[2]) in masks) and (int(subnet_mask[3]) in masks) and int(subnet_mask[0]) >= int(subnet_mask[1]) >= int(subnet_mask[2]) >= int(subnet_mask[3])):
                break

            else:
                print "Subnet mask error!! Please retry!!"
                continue

        
        # Convert subnet mask in binary
        mask_octet_padded = []
        mask_octet_decimal = subnet_mask

        #print mask_octet_decimal
        ''' 
        Written a function for this

        for octet_index in range(0, len(mask_octet_decimal)):

            #print bin(int(mask_octet_decimal[octet_index]))
            binary_octet = bin(int(mask_octet_decimal[octet_index])).split("b")[1]
            #print binary_octet

            # Check for length and add padded 0's

            if len(binary_octet) == 8:
                mask_octet_padded.append(binary_octet)

            elif len(binary_octet) < 8:
                binary_octet_padded = binary_octet.zfill(8)
                mask_octet_padded.append(binary_octet_padded)
        '''
        
        mask_octet_padded = convert_to_binary(mask_octet_decimal)

        decimal_mask = "".join(mask_octet_padded)
        #print decimal_mask  # this should print something like 255.255.255.0 -> 11111111111111111111111100000000

        # Lets count the number of 0's and 1's in the decimal mask

        number_of_zero = decimal_mask.count("0")
        number_of_ones = 32 - number_of_zero

        # To calculate the number of hosts in the network ->>> host = (2^n - 2)
        number_of_hosts = abs(2 ** number_of_zero - 2)

        #print number_of_zero
        #print number_of_ones
        #print number_of_hosts

        ## Calculate the wildcard mask

        wildcard_octets = []

        for wildcard in mask_octet_decimal:
            data = 255 - int(wildcard)
            wildcard_octets.append(str(data))

        wildcard_mask = ".".join(wildcard_octets)
        #print wildcard_mask

        ## Convert the IP to binary

        ip_octet_decimal = ip_add
        ip_octet_padded = convert_to_binary(ip_octet_decimal)
        binary_ip_add = "".join(ip_octet_padded)
        #print binary_ip_add

        ## Now lets get the network IP address and the broadcast IP address from the binary IP address

        network_ip_add_binary = binary_ip_add[:(number_of_ones)] + "0" * number_of_zero
        #print network_ip_add_binary

        broadcast_ip_add_binary = binary_ip_add[:(number_of_ones)] + "1" * number_of_zero
        #print broadcast_ip_add_binary

        # Get the network IP
        
        net_ip_octet = []
        for octet in range(0, len(network_ip_add_binary), 8):
            net_ip_oct = network_ip_add_binary[octet: octet+8]
            net_ip_octet.append(net_ip_oct)

        #print net_ip_octet
        # Get network IP
        
        network_ip = convert_to_decimal(net_ip_octet)
        network_address = ".".join(network_ip)
        #print network_address
        
        bdct_ip_octet = []
        for octet in range(0, len(broadcast_ip_add_binary), 8):
            bdct_ip_oct = broadcast_ip_add_binary[octet: octet+8]
            bdct_ip_octet.append(bdct_ip_oct)
 
        broadcast_ip = convert_to_decimal(bdct_ip_octet)
        broadcast_address = '.'.join(broadcast_ip)
        #print broadcast_address


        ## Resukts so far!!

        print "\n"
        print "Network address is %s " %network_address
        print "Broadcast address is %s " %broadcast_address
        print "Number of valid hosts in the network are %s " %number_of_hosts
        print "Wildcard mask is %s " %wildcard_mask
        print "\n"

        ### 
        # While loop that asks for random IP address!
        ###
        try:
            get_random_ip_address(network_ip, broadcast_ip)       
        except:
            print "Random IP address error..!!"


    except KeyboardInterrupt:
        print "Force closing the program!!"
        print "Bye!"



if __name__ == '__main__':
    Main()


