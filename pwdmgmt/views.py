from django.shortcuts import render
from usermgmt.utils import get_valid_user
from utils import get_password_by_sentence, get_dice_password


def password_generation(request):
    _user = get_valid_user(request)
    if request.method=="GET":
        return render(request, 'pwdmgmt_pwd_gen.html', {'current_user': _user})
    else:
        _sentence=request.POST.get("sentence","")
        if _sentence:
            _password=get_password_by_sentence(_sentence)
        else:
            _password=get_dice_password()
        return render(request, 'pwdmgmt_pwd_gen.html', {'current_user': _user, 'sentence':_sentence, 'password':_password})
