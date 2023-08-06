from setuptools import setup, find_packages 
  
long_description = 'Traceroute with Python for Windows'
  
setup( 
        name ='traceroute-win', 
        version ='1.7.0', 
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
        install_requires = ["scapy", "requests", "progressbar","python-firebase>=2.0.0beta"], 
        dependency_links=['https://github.com/ozgur/python-firebase/tarball/master#egg=python-firebase-2.0.0beta'],
        zip_safe = False
) 
