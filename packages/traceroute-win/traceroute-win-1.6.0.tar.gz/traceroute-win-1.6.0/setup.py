from setuptools import setup, find_packages 
  
long_description = 'Traceroute with Python for Windows'
  
setup( 
        name ='traceroute-win', 
        version ='1.6.0', 
        author ='Javed & Emeric', 
        author_email ='jsyedk@gmail.com', 
        description ='Traceroute with Python for Windows', 
        long_description = long_description, 
        long_description_content_type ="text/markdown", 
        license ='MIT', 
        packages = find_packages(), 
        entry_points ={ 
            'console_scripts': [ 
                'traceroute_win = traceroute_win.traceroute_win:main'
            ] 
        }, 
        classifiers =( 
            "Programming Language :: Python :: 3", 
            "License :: OSI Approved :: MIT License", 
            "Operating System :: OS Independent", 
        ), 
        keywords ='traceroute python package windows fastjaved', 
        install_requires = ["scapy", "requests", "progressbar"], 
        dependency_links=['https://github.com/ozgur/python-firebase@0d79d7609844569ea1cec4ac71cb9038e834c355'],
        zip_safe = False
) 
