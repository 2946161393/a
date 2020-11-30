#Muyi.Zhang
#9/21/2020
#CMPT221


from flask import Flask,request
from flask import render_template
app = Flask(__name__)

@app.route('/')
def folder(name=None):
    return render_template('form.html',name=name)

@app.route('/calculate_mortgage', methods=['GET'])
def poll_question():
    if request.method =='GET':
        yes = request.args.get("selection")
        no = request.args.get("selection")
        other = request.args.get("selection")
    else:
        # This is how we read off an input value from a POST request.  Here
        # "word_to_check is the name of the input variable defined in the
        # HTML form
        yes = request.form.get("word_to_check")
        no = request.form.get("word_to_check")
        other = request.form.get("word_to_check")
    yes = yes.strip()
    no = no.strip()
    other = yes.strip()

    if yes:
        return '<h1> {} was your answer</h1>'.format(yes)
        # Return an HTML document.  It does not need to be complete.
    return '<h1>{} was your answer</h1>'.format(yes)
   
    if no:
        return '{} was your answer</h1>'.format(no)
    return '{} was your answer</h1>'.format(no)


    if other:
        return '{} was your answer</h1>'.format(no)
    return '{} was your answer</h1>'.format(other)

        


if __name__ == "__main__":
    app.run()

