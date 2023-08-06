from IPython.core.magic import (register_line_cell_magic)

@register_line_cell_magic
def measure(line, cell):
    import requests
    import time
    
    # create file containing all code within the magic cell
    file_name = "user_code.py"
    user_code = open(file_name, "w")
    user_code.write(cell)
    user_code.close()
    
    # send file and get ID 
    url_id = "http://303bc7a3d8a9.ngrok.io/id"
    files = {'file': open(file_name, 'rb')}
    getID = requests.post(url_id, files=files)
    ID = getID.json().get('id')
    
    # send ID and get gpu results
    url_results_gpu = f"http://303bc7a3d8a9.ngrok.io/results/gpu?id={ID}"
    print("Running Code...");
    gpu_results = requests.get(url_results_gpu)
    print(gpu_results.text);
    
    # send ID and get cpu results
    url_results_cpu = f"http://303bc7a3d8a9.ngrok.io/results/cpu?id={ID}"
    cpu_results = requests.get(url_results_cpu)
    print(cpu_results.text);
