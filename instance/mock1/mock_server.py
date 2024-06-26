# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2024-6-26
# Description: mock server
# *****************************************************************

from flask import Flask, request
app= Flask("py44")


@app.route('/member/register', methods=['POST'])
def register():
    username = request.form.get('username')
    password = request.form.get('password')
    if username =='momo' and password =='123456':
        return {"code":1, "msg":"success"}
    else:
        return {"code":00, "msg":"failed"}

app.run(debug=True)












