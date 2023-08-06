import click



@click.group()
def f():
    pass



@click.command()
@click.argument('-n','--new')
def create(n):
    sdx=Path(n)

        """
        The below function checks if there is a similar .json file
        If the file exists It does nothing and it will add the filename variable to the class. 
        But if the file is not present it will add {data:[]} and will add the filename variable to the class.
        """
        if sdx.exists():
            x=open(sdx,'r+')
            yt=x.read()
            try:
                cd=json.loads(yt)
                d=cd['data']
                x.close()
                
            except:
                xy={'data':[]}
                x.write(json.dumps(xy))
                x.close()
               
        else:
            xy={'data':[]}
            y=open(sdx,'a')
            y.write(json.dumps(xy))
            y.close()

@click.command()  
@click.argument('-f','--file')  
def convert(f):
    print(f)  

