from django.shortcuts import render
from rest_framework.generics import CreateAPIView,ListAPIView,RetrieveAPIView,UpdateAPIView,DestroyAPIView
from app.serializers import UserSerializer,ProfileSerializer,FoodlogSerializer
from rest_framework import authentication,permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from app.models import Profile,FoodLog,Subscription
from django.utils import timezone
from datetime import timedelta
from rest_framework_simplejwt.authentication import JWTAuthentication
from app.utility import analyze_food,generate_kerala_diet_plan
from app.permissions import HasProfile
from django.db.models import Sum
import razorpay

RZP_API_KEY="rzp_test_TbuqWchCl5EbCq"
RZP_KEY_SECRET="LMuwBkH4DZgX1FDgNSf0gXTW"


# Create your views here.
class UserCreateView(CreateAPIView):
    serializer_class=UserSerializer

class ProfileCreateListView(CreateAPIView,ListAPIView):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    serializer_class=ProfileSerializer

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)
# class ProfileDetailView(APIView):
#     authentication_classes=[authentication.TokenAuthentication]
#     permission_classes=[permissions.IsAuthenticated]

#     def get(self,request,*args,**kwargs):
#         user_instance=request.user
#         profile_instance=user_instance.user_profile
#         print(user_instance)
#         print(profile_instance)
#         serializer=ProfileSerializer(profile_instance)
#         return Response(serializer.data)

class ProfileDetailView(RetrieveAPIView,UpdateAPIView):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    serializer_class=ProfileSerializer

    def get_object(self):
        return self.request.user.user_profile

class FoodLogCreateListView(CreateAPIView,ListAPIView):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    serializer_class=FoodlogSerializer
    # query_set=FoodLog.objects.all()
    
    def perform_create(self,serializer):
        return serializer.save(user=self.request.user) 

    # def get(self,request,*args,**kwargs):
    #     user_instance=request.user
    #     food_list=user_instance.food_log.all()
    #     # food_log.objects.filter(user=user_instance)
    #     serializer=FoodlogSerializer(food_list,many=True)
    #     return Response(data=serializer.data)

    # def get_queryset(self):
    #     cur_date=timezone.now().date()
    #     print(cur_date)
    #     # return FoodLog.objects.filter(user=self.request.user,created_at=cur_date)
        # return self.request.user.food_log.filter(created_at_date=cur_date)
        # return self.request.user.food_log.all()

    def get_queryset(self):
        cur_date=timezone.now().date()
        print(cur_date)
        yesterday=cur_date-timedelta(days=1)
        print(yesterday)
        last_week=cur_date-timedelta(days=7)
        params=self.request.query_params
        if "start_date" and "end_date" in self.request.query_params:
            start_date=params.get("start_date")
            end_date=params.get("end_date")
            return self.request.user.food_log.filter(created_at__date__gte=start_date,created_at__date__lte=end_date)
        if "filter_type" in params:
            if params['filter_type']=='yesterday':
                return self.request.user.food_log.filter(created_at__date=yesterday)
            
            elif params['filter_type']=='last_week':
                return self.request.user.food_log.filter(created_at__date__gte=last_week,created_at__date__lte=cur_date)
        return self.request.user.food_log_filter(created_at__date=cur_date)


    
    
# # class FoodLogDetailView(APIView):
#     authentication_classes=[authentication.TokenAuthentication]
#     permission_classes=[permissions.IsAuthenticated]

#     def get(self,request,*args,**kwargs):
#         id=kwargs.get("id")
#         food=FoodLog.objects.get(id=id)
#         serializer=FoodlogSerializer(food)
#         return Response(data=serializer.data)

# class FoodLogDetailView(RetrieveAPIView,UpdateAPIView,DestroyAPIView):
#     authentication_classes=[authentication.TokenAuthentication]
#     permission_classes=[permissions.IsAuthenticated]
#     serializer_class=FoodlogSerializer
#     queryset=FoodLog.objects.all()
#     lookup_url_kwarg="id"

class FoodLogDetailView(RetrieveAPIView,UpdateAPIView,DestroyAPIView):
    authentication_classes=[JWTAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    serializer_class=FoodlogSerializer
    queryset=FoodLog.objects.all()
    lookup_url_kwarg="id"


class FoodScanView(APIView):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    def post(self,request,*args,**kwargs):
        form_data=request.data
        print(form_data)
        image=form_data.get("image")
        try:
            res=analyze_food(image)
            print(res)
            title=res.get("food_name")
            calorie=res.get("average_calorie")
            meal_type=res.get("meal_type")
            food=FoodLog.objects.create(title=title,calorie=calorie,meal_type=meal_type,user=request.user,image=image)
            serializer=FoodlogSerializer(food)
            return Response(data=serializer.data)
        except Exception as e:
            print(e)
        return Response({"msg":"image scanning...."})

class DietPlanView(APIView):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated,HasProfile]

    def post(self,request,*args,**kwargs):
        profile=request.user.user_profile
        age=profile.age
        gender=profile.gender
        weight=profile.weight
        form_instance=request.data
        goal=form_instance.get("goal")
        duration=form_instance.get("duration")
        target=form_instance.get("target_weight")
        try:
            res=generate_kerala_diet_plan(goal,age,weight,gender,target,duration)
            print(res)
            return Response(data=res)
        except Exception as e:
            print(e)
        return Response({"msg":"diet plan"})

class SummaryView(APIView):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated,HasProfile]
    # def get(self,request,*args,**kwargs):
    #     profile=request.user.user_profile
    #     daily=profile.daily_calorie_goal
    #     # print(profile.daily_calorie_goal)
    #     # total_consumed=0
    #     # for f in food:
    #     #     total_consumed+=f.calories
    #     #     print(f.calories)
    #     # print(total_consumed)
    #     cur_date=timezone.now().date()
    #     food=request.user.food_log.filter(created_at__date=cur_date)
    #     consumed=food.values("calorie").aggregate(total=Sum("calorie")).get("total") or 0
    #     meal_type_calories=food.values("meal_type").annotate(total=Sum("calorie"))
    #     remaining=daily-consumed

    #     context={"Daily_calorie_goal":daily,
    #              "Consumed_calories":consumed,
    #              "Remaining":remaining,
    #              "meal_based_calories":meal_type_calories
    #     }

    #     return Response(data=context)
    
    def get(self,request,*args,**kwargs):
            profile=request.user.user_profile
            daily=profile.daily_calorie_goal
            cur_date=timezone.now().date()
            qs=request.user.food_log.filter(created_at__date=cur_date)
            params=request.query_params
            if params:
                if "filter_type" in params:
                    if params['filter_type']=="yesterday":
                        yesterday=cur_date-timedelta(days=1)
                        qs=request.user.food_log.filter(created_at__date=yesterday)
                    if params['filter_type']=="last_week":
                        start_date=cur_date-timedelta(days=7)
                        qs=request.user.food_log.filter(created_at__date__gte=start_date,created_at__date__lte=cur_date)
                        weekly_goal=profile.daily_calorie_goal*7
                        consumed=qs.values("calorie").aggregate(total=Sum("calorie")).get("total") or 0
                        meal_type_calories=qs.values("meal_type").annotate(total=Sum("calorie"))
                        remaining=weekly_goal-consumed 
                        
                        context={"Weekly_calorie_goal":weekly_goal,
                                             "Consumed_calories":consumed,
                                             "Remaining":remaining,
                                             "meal_based_calories":meal_type_calories
                                    }                 
           
            return Response(data=context)

class PaymentCreateView(APIView):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated,HasProfile]

    def post(self,request,*args,**kwargs):
        
        client = razorpay.Client(auth=(RZP_API_KEY,RZP_KEY_SECRET))
        amount=599
        amount_in_paisa=amount*100
        DATA = {
                "amount":amount_in_paisa,
                "currency": "INR",
                "receipt": "receipt#1",
                "notes": {
                    "key1": "value3",
                    "key2": "value2"
                                    }
                }
        payment=client.order.create(data=DATA)
        print(payment)
        
        razorpay_order_id=payment.get("id")
        Subscription.objects.create(user=request.user,razorpay_order_id=razorpay_order_id,amount=amount)
        
        return Response({'msg':'payment pending'})
    
class VerifyPayment(APIView):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated,HasProfile]
    def post(self,request,*args,**kwargs):
        razorpay_order_id=request.data.get("razorpay_order_id")
        razorpay_payment_id=request.data.get("razorpay_payment_id")
        razorpay_signature=request.data.get("razorpay_signature")

        sub=Subscription.objects.get(user=request.user,status="PENDING")
        client = razorpay.Client(auth=(RZP_API_KEY,RZP_KEY_SECRET))

        client.utility.verify_payment_signature({
                        'razorpay_order_id': razorpay_order_id,
                        'razorpay_payment_id': razorpay_payment_id,
                        'razorpay_signature': razorpay_signature
        })
        start_date=timezone.now().date()
        expiry_date=start_date+timedelta(days=30)
        sub.start_date=start_date
        sub.expiry_date=expiry_date
        sub.status="ACTIVE"
        sub.razorpay_payment_id=razorpay_payment_id
        sub.save()
        return Response({'msg':'Subscription active now'})