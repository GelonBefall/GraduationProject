# import argparse
import json
import requests
import time
import os


# def pdb_to_hssp(pdbID):
#     rest_url="http://www.cmbi.umcn.nl/xssp/"
#     # Read the pdb file data into a variable
#     # __pdbPath = "./materials/pdb/"
#     # __pdbFile = os.path.join(__pdbPath, "{}.pdb".format(pdbID))
#     __dsspPath = "./materials/dssp/"
#     __dsspFile = os.path.join(__dsspPath, "{}.dssp".format(pdbID))
#     data={'pdb_id':pdbID}
#     # files = {'file_': open(__pdbFile, 'rb')}

#     # Send a request to the server to create hssp data from the pdb file data.
#     # If an error occurs, an exception is raised and the program exits. If the
#     # request is successful, the id of the job running on the server is
#     # returned.
#     url_create = '{}api/create/pdb_id/dssp/'.format(rest_url)
#     r = requests.post(url_create, data=data)
#     r.raise_for_status()

#     job_id = json.loads(r.text)['id']
#     print ("Job submitted successfully. Id is: '{}'".format(job_id))

#     # Loop until the job running on the server has finished, either successfully
#     # or due to an error.
#     ready = False
#     while not ready:
#         # Check the status of the running job. If an error occurs an exception
#         # is raised and the program exits. If the request is successful, the
#         # status is returned.
#         url_status = '{}api/status/pdb_id/dssp/{}/'.format(rest_url,
#                                                                   job_id)
#         r = requests.get(url_status)
#         r.raise_for_status()

#         status = json.loads(r.text)['status']
#         print ("Job status is: '{}'".format(status))

#         # If the status equals SUCCESS, exit out of the loop by changing the
#         # condition ready. This causes the code to drop into the `else` block
#         # below.
#         #
#         # If the status equals either FAILURE or REVOKED, an exception is raised
#         # containing the error message. The program exits.
#         #
#         # Otherwise, wait for five seconds and start at the beginning of the
#         # loop again.
#         if status == 'SUCCESS':
#             ready = True
#         elif status in ['FAILURE', 'REVOKED']:
#             raise Exception(json.loads(r.text)['message'])
#         else:
#             time.sleep(5)
#     else:
#         # Requests the result of the job. If an error occurs an exception is
#         # raised and the program exits. If the request is successful, the result
#         # is returned.
#         url_result = '{}api/result/pdb_id/dssp/{}/'.format(rest_url, job_id)
#         r = requests.get(url_result)
#         r.raise_for_status()
#         result = json.loads(r.text)['result']
#         with open(__dsspFile,"wb") as dsspFile:
#             dsspFile.write(result)
#         # Return the result to the caller, which prints it to the screen.
#         return result

