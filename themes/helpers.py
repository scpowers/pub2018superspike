'''
helpers - helper methods that are called in other files to minimize
repeated code blocks.
'''
import numpy as np

# ndarray2ras - converts a 2D ndarray of numeric values into a .ras file
def ndarray2ras(output_filename, input_matrix, numExtraDigits, numDecimalPlaces, dt):

    num_rows = input_matrix.shape[0]
    print('number of rows in output: ', num_rows)
    num_coeffs = input_matrix.shape[1]
    print('number of coefficients per row: ', num_coeffs)

    '''
    Convert the output matrix into the .ras file format.
    Each line consists of a ('spike_time' 'neuronID') pair.
    For each coefficient, it has numExtraDigits + 1 sets of 10 neurons 
    for the digits before the decimal place (baseline has 1's place)
    and numDecimalPlaces sets of 10 neurons for decimal places.
    Each coefficient also has one polarity neuron (spikes if negative),
    which yields a total of (10*(numExtraDigits+1) + 10*(numDecimalPlaces) + 1)
    neurons per coefficient
    '''
    # start writing to file
    with open('%s.ras'%output_filename, 'w') as f:
        
        # compute number of neurons per group (or coefficient) for later
        nPerCoeff = 1 + (10 * (numExtraDigits+1)) + (10 * numDecimalPlaces)
        
        # loop over rows of coefficients
        for row in range(num_rows):
            
            # reset the index of the neuron marking the beginning of the
            # set of 10 neurons representing a single digit in a coefficient
            # because each coefficient starts with a polarity bit, the first
            # neuron that loops will consider is neuron #2
            setStartNeuron = 1

            # loop over coefficients in a row
            for coeff in range(num_coeffs):
                # the value to convert
                val = input_matrix[row, coeff]

                # first check if the polarity neuron needs to spike (if negative)
                # polarity neuron is the first neuron in a group, where each
                # group represents a single coefficient value
                if val < 0:
                    f.write('%f %i\n'%(dt*row, setStartNeuron ))

                # now shift the starting index by 1 to move past the polarity neuron
                setStartNeuron += 1

                # now work with absolute value of val
                val = abs(val)
                    
                # considers 1's place at the minimum (numExtraDigits=0)
                for i in range(numExtraDigits+1, 0, -1):
                    # compute the value of the digit from left to right
                    temp = (val % 10 ** i) // 10 ** (i-1)
                    #print('it found value ', temp, ' in the pre-radix')
                    #if (setStartNeuron + int(temp) == 155):
                        #print('found weird spot')
                        #print('row: ', row)
                        #print('coeff: ', coeff)
                        #print('i: ', i)
                        #print('setStartNeuron: ', setStartNeuron)
                        #print('temp: ', temp)
                    f.write('%f %i\n'%(dt*row, setStartNeuron + int(temp)))

                    # update the neuron marking the start of the set of 11 
                    setStartNeuron += 10

                # now consider decimal places
                for i in range(numDecimalPlaces):
                    #print('i = ', i)
                    # compute the value of the digit from left to right
                    temp = ((((val * 10 ** (i+1)) % 10 ** (i+1)) % 10 ** 1) + 0.000000001) // 1
                    #print('operation 1: ', val * 10 ** (i+1))
                    #print('operation 2: ', ((val * 10 ** (i+1)) % 10 ** (i+1)))
                    #print('operation 3: ', ((val * 10 ** (i+1)) % 10 ** (i+1)) % 10 ** 1)
                    #print('operation 4: ', temp)
                    #print('it found value ', temp, ' in the post-radix')
                    #if (setStartNeuron + int(temp) == 155):
                        #print('found weird spot')
                        #print('row: ', row)
                        #print('coeff: ', coeff)
                        #print('i: ', i)
                        #print('setStartNeuron: ', setStartNeuron)
                        #print('temp: ', temp)
                    f.write('%f %i\n'%(dt*row, setStartNeuron + int(temp)))
                    
                    # update the neuron marking the start of the set of 11 
                    setStartNeuron += 10

                # now update the set start neuron for the next coefficient
                #setStartNeuron += 1


# ras2ndarray - converts a .ras file into a 2D ndarray of numeric values
def ras2ndarray(output_filename, input_ras, numCoeffs, numExtraDigits, numDecimalPlaces, 
        numSteps, dt):

        # compute number of neurons per group (or coefficient) for later
        nPerCoeff = 1 + (10 * (numExtraDigits+1)) + (10 * numDecimalPlaces)
        print('number of neurons per coefficient: ', nPerCoeff)
                    
        # initialize the output array as 1's so you can flip the polarity
        # just means you have to subtract 1 from every coefficient at the end
        output = np.ones((numSteps, numCoeffs))

        # start the reference timer
        t_ref = 0.0

        # start the time switch flag
        same_time = True

        # start the row counter
        row = 0

        # start the reference coefficient
        coeff_ref = 0

        # start the same coefficent flag
        same_coeff = True

        # start the is_negative flag
        is_neg = False

        with open(input_ras, 'r') as f: # This closes the file for you when you are done

            # look at lines one at a time
            for line in f:
                
                # separate the two values
                vals = line.split()
                time = float(vals[0])
                neuron = int(vals[1])
                #print('looking at time: ', time, ', neuron: ', neuron)
                
                # determine what time step you're working with
                if time != t_ref:
                    t_ref = time
                    same_time = False
                    row += 1
                else:
                    same_time = True

                #print('current row val: ', row)
                
                # determine what coefficient you're working with
                coeff = int(np.ceil(neuron / nPerCoeff) - 1)
                #print('this neuron corresponds to a digit in coeff: ', coeff)

                # update the reference coefficient flag, if necessary
                if coeff != coeff_ref:
                    same_coeff = False
                    
                    # update the reference coefficient
                    coeff_ref = coeff
                
                # means you're still working on the same coefficient
                else:
                    same_coeff = True
                

                # determine which digit you're working with
                
                # first check to see if you landed on a polarity neuron spike
                if ((neuron - 1) % nPerCoeff) == 0:
                    #print('found a negative coefficient')
                    #print('neuron: ', neuron)
                    #print('row: ', row)
                    #print('coeff: ', coeff)
                    output[row, coeff] *= -1
                    is_neg = True

                # this means you're working with an actual digit value
                else:
                    # if you switched to a new coefficient without encountering
                    # a polarity neuron, it's not negative
                    if same_coeff == False or same_time == False:
                        is_neg = False
                        
                    # drop the neuron count to between 0-(nPerCoeff-1)
                    neuron -= (coeff * nPerCoeff + 2)

                    # check if it's a pre-radix digit
                    pos = neuron // 10
                    if pos <= numExtraDigits:
                        
                        # update the coefficient at this time step
                        if (is_neg == False):
                            output[row, coeff] += ( (neuron % 10) * (10 ** (numExtraDigits - pos)) ) 
                            #print('interpreted ', neuron, ' as: ', ( (neuron % 10) * (10 ** (numExtraDigits - pos)) ))
                            if time > 65877:
                                print('interpreted ', neuron, ' as: ', ( (neuron % 10) * (10 ** (numExtraDigits - pos)) ))
                                
                        else:
                            output[row, coeff] -= ( (neuron % 10) * (10 ** (numExtraDigits - pos)) ) 
                            #print('interpreted ', neuron, ' as: ', ( (neuron % 10) * (10 ** (numExtraDigits - pos)) ))

                    # means it's a post-radix digit
                    else:
                        
                        # update the coefficient at this time step
                        if (is_neg == False):
                            output[row, coeff] += ( (neuron % 10) * (10 ** -(pos - numExtraDigits)) )
                            #print('interpreted ', neuron, ' as: ', ( (neuron % 10) * (10 ** -(pos - numExtraDigits)) )) 
                        else:
                            output[row, coeff] -= ( (neuron % 10) * (10 ** -(pos - numExtraDigits)) )
                            #print('interpreted ', neuron, ' as: ', ( (neuron % 10) * (10 ** -(pos - numExtraDigits)) )) 

        print(output[-10:,:])
        # now subtract the initial 1 from initializing it as a 1's array
        for step in range(numSteps):
            for c in range(numCoeffs):
                if output[step, c] < 0:
                    output[step,c] += 1
                else:
                    output[step,c] -= 1
                        
        
        print(output[-10:,:])
        # print out vals, just for debugging
        #print(output)

        # save and return output
        np.save(output_filename + '.npy', output)
        return output
                            
        
                
                
            
        

