from django.shortcuts import render, reverse, HttpResponseRedirect, redirect
from bugtracker.forms import LoginForm, AddUserForm, TicketF, EditTicketF
from bugtracker.models import MyUser, TicketM
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from config.settings import AUTH_USER_MODEL
from django.contrib.auth.decorators import login_required


@login_required
def homepage_view(request):
    tickets = TicketM.objects.all().order_by('-time')
    user = request.user
    new_tickets = TicketM.objects.filter(choose_stat="New")
    completed_tickets = TicketM.objects.filter(choose_stat="Done")
    in_progress = TicketM.objects.filter(choose_stat="In Progress")
    invalid = TicketM.objects.filter(choose_stat="Invalid")
    return render(
        request,
        'homepage.html', 
        {'user': user, 
            "user_model": AUTH_USER_MODEL,
            "tickets": tickets,
            "new_tickets": new_tickets,
            "completed_tickets": completed_tickets,
            "in_progress": in_progress,
            "invalid": invalid
        }
    )

# @login_required
def edit_ticket_view(request, ticket_id):
    item = TicketM.objects.get(id=ticket_id)
    if request.method == "POST":
        form = EditTicketF(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            item.title = data['title']
            item.description = data["description"]
            item.save()
            return HttpResponseRedirect(reverse('ticket_detail', args=(ticket_id,)))
    form = EditTicketF(initial={
        "title": item.title,
        "description": item.description
    })
    return render(request, "form.html", {"form": form})


@login_required
def assign_view(request, ticket_id):
    ticket = TicketM.objects.get(id=ticket_id)
    ticket.choose_stat = 'In Progress'
    ticket.user_assigned_to_ticket = request.user
    ticket.user_completed_ticket = None
    ticket.save()
    return redirect(
        ticketdetail_view,
        ticket_id=ticket_id
    )


@login_required
def completed_view(request, ticket_id):
    ticket = TicketM.objects.get(id=ticket_id)
    ticket.choose_stat = 'Done'
    ticket.user_assigned_to_ticket = None
    ticket.user_completed_ticket = request.user
    ticket.save()
    return redirect(
        ticketdetail_view,
        ticket_id=ticket_id
    )


@login_required
def invalid_view(request, ticket_id):
    ticket = TicketM.objects.get(id=ticket_id)
    ticket.choose_stat = 'Invalid'
    ticket.user_assigned_to_ticket = None
    ticket.user_completed_ticket = None
    ticket.save()
    return redirect(
        ticketdetail_view,
        ticket_id=ticket_id
    )


@login_required
def addticket_view(request):
    if request.method == "POST":
        form = TicketF(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            TicketM.objects.create(
                title=data["title"],
                description=data["description"],
                created_by=request.user
            )
            return redirect("/")
    form = TicketF()
    return render(request, 'form.html', {"form": form})


@login_required
def userdetail_view(request, user_id):
    user = MyUser.objects.get(id=user_id)
    created_tickets = TicketM.objects.filter(created_by=user)
    assigned_tickets = TicketM.objects.filter(
        user_assigned_to_ticket=user,
        # choose_stat="New"
    )
    completed_tickets = TicketM.objects.filter(user_completed_ticket=user)
    return render(
        request, 
        'userdetail.html',
        {'user': user, 
            "user_model": AUTH_USER_MODEL,
            "created_tickets": created_tickets,
            "assigned_tickets": assigned_tickets,
            "completed_tickets": completed_tickets
        }
    )


@login_required
def ticketdetail_view(request, ticket_id):
    ticket = TicketM.objects.get(id=ticket_id)
    return render(request, 'ticketdetail.html', {"ticket": ticket})


def login_view(request):
   if request.method == "POST":
       form = LoginForm(request.POST)
       if form.is_valid():
           data = form.cleaned_data
           user = authenticate(
               request, username=data["username"], password=data["password"]
           )
           if user:
               login(request, user)
               return HttpResponseRedirect(
                   request.GET.get("next", reverse("home"))
               )
 
   form = LoginForm()
   return render(request, 'login.html', {"form": form})
 

@login_required
def logout_view(request):
   logout(request)
   return redirect("home")
