#!/usr/bin/python


def outlierCleaner(predictions, ages, net_worths):
    """
        clean away the 10% of points that have the largest
        residual errors (different between the prediction
        and the actual net worth)

        return a list of tuples named cleaned_data where 
        each tuple is of the form (age, net_worth, error)
    """
    numToKeep = int(len(predictions)*0.9)

    data = [(a[0],n[0],e[0]) for a,n,e in zip(ages,net_worths,abs(predictions-net_worths))]
    #print data[:5]
    sorted_data = sorted(data,key=lambda sort_this: sort_this[2])
    #print sorted_data[:5]
    cleaned_data = sorted_data[:numToKeep]
    #print len(cleaned_data)
    ### your code goes here

    
    return cleaned_data

