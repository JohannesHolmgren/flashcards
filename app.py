from flask import Flask, render_template
from markupsafe import escape


frontsides = ["What does the Inertial Navigation System (INS) use to estimate the robot's states?", 'What is the acceleration in world frame transformed into before being transformed back again?', 'What is the linear kinematics equation for the $x$-axis in the state estimation model?', 'How is the acceleration in the $z$-direction calculated relative to gravity?', 'What is the equation for angular kinematics on the $z$-axis in the state estimation model?', 'another question', 'another question', 'another question'][0:3]
backsides = ['Extended Kalman Filter', 'Robot Frame', '$$\\mathbf{\\hat{X}}_{x,k|k-1} = \\begin{bmatrix} x_{k-1|k-1} + \\dot{x}_{k-1|k-1}\\Delta t + \\frac{1}{2}(\\Delta t)^2(u_{x,k}\\cos\\psi - u_{y,k} \\sin\\psi) \\\\ \\dot{x}_{k-1|k-1} + \\Delta t (u_{x,k}\\cos\\psi - u_{y,k}\\sin\\psi) \\end{bmatrix}$$', '$$\\mathbf{\\hat{X}}_{z,k|k-1} = \\begin{bmatrix} z_{k-1|k-1} + \\dot{z}_{k-1|k-1}\\Delta t + \\frac{1}{2}(\\Delta t)^2(u_{z,k} - G) \\\\ \\dot{z}_{k-1|k-1} + \\Delta t (u_{z,k} - G) \\end{bmatrix}$$', '$$\\mathbf{\\hat{X}}_{\\psi,k|k-1} = \\begin{bmatrix} \\psi_{k-1|k-1} + \\Delta tu_{\\psi,k} \\\\ u_{\\psi,k} \\end{bmatrix}$$', 'another question', 'another question', 'another question'][0:3]

app = Flask(__name__)

@app.route('/')
def hello_world():
    return f'<p>Hello World!<p>'

@app.route('/<name>')
def hello_world2(name):
    return f'<p>Hello {escape(name)}<p>'

@app.route('/cards')
def cards():
    return render_template("index.html", content=list(zip(frontsides, backsides)))