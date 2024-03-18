from django.shortcuts import render, redirect
from django.core.validators import validate_email
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

from django.http import HttpResponseForbidden
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
import codecs

from django.http import JsonResponse
# Create your views here.

def sing_in(request):

    if request.method == "POST":
        email = request.POST.get('email', None)
        password = request.POST.get('password', None)

        user = User.objects.filter(email=email).first()
        if user:
            auth_user = authenticate(username=user.username, password=password)
            if auth_user:
                login(request, auth_user)
                return redirect('dashboard')
            else:
                print("mot de pass incorrecte")
        else:
            print("User does not exist")

    return render(request, 'login.html', {})

def sing_up(request):
    error = False
    message = ""
    if request.method == "POST":
        name = request.POST.get('name', None)
        email = request.POST.get('email', None)
        password = request.POST.get('password', None)
        repassword = request.POST.get('repassword', None)
        # Email
        try:
            validate_email(email)
        except:
            error = True
            message = "Enter un email valide svp!"
        # password
        if error == False:
            if password != repassword:
                error = True
                message = "Les deux mot de passe ne correspondent pas!"
        # Exist
        user = User.objects.filter(Q(email=email) | Q(username=name)).first()
        if user:
            error = True
            message = f"Un utilisateur avec email {email} ou le nom d'utilisateur {name} exist déjà'!"
        
        # register
        if error == False:
            user = User(
                username = name,
                email = email,
            )
            user.save()

            user.password = password
            user.set_password(user.password)
            user.save()

            return redirect('sing_in')

    context = {
        'error':error,
        'message':message
    }
    return render(request, 'register.html', context)


@login_required(login_url='sing_in')
def dashboard(request):
    return render(request, 'admin.html', {})

def log_out(request):
    logout(request)
    return redirect('sing_in')



def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        
        user = User.objects.filter(email=email).first()
        
        if user:
            print("send eemail")
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            current_site = request.META['HTTP_HOST']
            context = {
                "token":token,
                "uid":uid,
                "domaine":f"http://{current_site}"
            }
            
            html_text = render_to_string("email.html", context)
            msg = EmailMessage(
                "Test Send email django use template",
                html_text,
                "NISCG <nisconsultingci@gmail.com>",
                [user.email]
            )
            
            msg.content_subtype = "html"
            msg.send()
            
        else:
            print("user does not exist")
        
    return render(request, 'forgot_password.html', {})


def update_password(request, token, uid):
    try:
        user_id = urlsafe_base64_decode(uid)
        decode_uid = codecs.decode(user_id, 'utf-8')
        user = User.objects.get(id=decode_uid)
    except:
        return HttpResponseForbidden("Vous n'aviez pas la permission de modifier ce mot de pass. Utilisateur introuvable")
    
    check_token = default_token_generator.check_token(user, token)
    if not check_token:
        return HttpResponseForbidden("Vous n'aviez pas la permission de modifier ce mot de pass. Votre Token est invalid ou a espiré")
    
    error = False
    success = False
    message = ""
    if request.method == "POST":
        password = request.POST.get("password")
        repassword = request.POST.get("repassword")
        print(password , repassword)
        if repassword == password:
            try:
                validate_password(password, user)
                user.set_password(password)
                user.save()
                
                success = True
                message = "votre mot de pass a été modifié avec succès!"
            except ValidationError as e:
                error = True
                message = str(e)
        else:
            error = True
            message = "Les deux mot de pass ne correspondent pas"
            
    context = {
        "error": error,
        "success": success,
        "message": message
    }
    
    return render(request, 'update_password.html', context)



def send_mail_awsuga(request):
    user_emails = [
        {'Nom': 'Fatayo Sodiki Aderemi Ope', 'email': 'sodikfatayo@gmail.com'},
        {'Nom': 'Sidoine KRA', 'email': 'sidoinekra@gmail.com'},
        {'Nom': 'BOIDI Eric', 'email': 'boidiaka@gmail.com'},
        {'Nom': 'Yesso', 'email': 'yesso.aho19@inphb.ci'},
        {'Nom': 'KRA KOUASSI JACOB', 'email': 'krakouassijacob@yahoo.fr'},
        {'Nom': 'Sadialiou Diallo', 'email': 'seriadiallo1@gmail.com'},
        {'Nom': 'Lionel Money', 'email': 'lionelandy95@gmail.com'},
        {'Nom': 'Aimé', 'email': 'aimanuelaka@gmail.com'},
        {'Nom': 'Getheme brika', 'email': 'gethemebrika@gmail.com'},
        {'Nom': 'YAO De-jacques Jean-Baptiste', 'email': 'yaodejacques@gmail.com'},
        {'Nom': 'Epinzagne ivan cesar', 'email': 'epinzagnetresorivan@gmail.com'},
        {'Nom': 'Kevin  KONE', 'email': 'kevinkone19@gmail.com'},
        {'Nom': 'Koffi Bi Blin Modeste Junior', 'email': 'modestekoffi005@gmail.com'},
        {'Nom': 'Galogbe', 'email': 'Galogbe.djessa@gmail.com'},
        {'Nom': 'DJAMA Med', 'email': 'd.lemec93@live.fr'},
        {'Nom': 'Samaké Mamery', 'email': 'saryma90@gmail.com'},
        {'Nom': 'Goms', 'email': 'hackmmn@gmail.com'},
        {'Nom': 'Nikiema', 'email': 'nikiemaismael2020@gmail.com'},
        {'Nom': 'Alder Laroche', 'email': 'monneylaroche@gmail.com'},
        {'Nom': 'loïc Akatcha', 'email': 'loicakatcha12@gmail.com'},
        {'Nom': 'Guei Éric Nicaise', 'email': 'nicoclassique@hotmail.fr'},
        {'Nom': 'Marie Estelle', 'email': 'bandamapascale@gmail.com'},
        {'Nom': 'Thierno DIOP', 'email': 'thiernodiop.diop@gmail.com'},
        {'Nom': 'KOUAKOU Yves Armand', 'email': 'yvesarmand02@gmail.com'},
        {'Nom': 'Kouame kouakou jean-yves', 'email': 'jeanyves.kouame@outlook.fr'},
        {'Nom': 'Achi achou Wilfried junior', 'email': 'coachwilfriedjrachi@gmail.com'},
        {'Nom': 'KOUTOUAN MATHIAS', 'email': 'koutouangcp225@gmail.com'},
        {'Nom': 'KONATÉ CHRISTOPHE JEAN-BAPTISTE', 'email': 'christjessusnouna@Gmail.com'},
        {'Nom': 'Tanoh Bonzou serge philippe', 'email': 'sergetanoh13@gmail.com'},
        {'Nom': 'Allasane Gueye', 'email': 'gueyealassaneharouna@gmail.com'},
        {'Nom': 'serge kotta', 'email': 'sergekota@gmail.com'},
        {'Nom': 'Jacques', 'email': 'succes_jacques@yahoo.com'},
        {'Nom': 'Ismael Seck', 'email': 'ismaelseck11@gmail.com'},
        {'Nom': 'Romaric Saulet', 'email': 'romaricsaulet@gmail.com'},
        {'Nom': 'dorra taouali', 'email': 'dorrataouali@gmail.com'},
        {'Nom': 'Meite tiemoko', 'email': 'Meitetiemoko@gmail. Com'},
        {'Nom': 'Etienne DIBI', 'email': 'etiennedibi@gmail.com'},
        {'Nom': 'Ouattara Daouda', 'email': 'ouattara.daouda4613@gmail.com'},
        {'Nom': 'Bakary SAMAKE', 'email': 'samakebakary036@gmail.com'},
        {'Nom': 'Joël Konan', 'email': 'Joel.Konan101@gmail.com'},
    ]
    meet_url = "https://www.youtube.com/watch?v=9ecvdCKm9As"
    for user in user_emails:
        context = {
            "meet_url":meet_url,
            "nom": user.get('Nom')
        }
        
        html_text = render_to_string("email_aws_ug.html", context)
        msg = EmailMessage(
            "🌟 Événement AWS User Group Abidjan : Introduction au Cloud AWS 🚀",
            html_text,
            "AWS User Group Abidjan <awsabidjanusergroup@gmail.com>",
            [user.get('email')]
        )
        try:
            msg.content_subtype = "html"
            msg.send()
        except Exception as e:
            print(str(e))
    return JsonResponse({})