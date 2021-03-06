from django import forms
from django.core import validators


# ทำให้ใส่ได้แค่เลขคู่
from django.core.exceptions import ValidationError

from polls.models import Poll, Question, Choice


def validate_even(value):
    if value % 2 != 0:
        raise ValidationError('%(value)s ไม่ใช่เลขคู่', params={'value': value})


class PollForm(forms.Form):
    title = forms.CharField(label="ชื่อโพล", max_length=100, required=True)

    email = forms.CharField(validators=[validators.validate_email])
    no_questions = forms.IntegerField(label="ชื่อจำนวนคำถาม", min_value=0, max_value=10, required=True, validators=[validate_even])

    start_date = forms.DateField(required=False)
    end_date = forms.DateField(required=False)

    def clean_title(self):
        data = self.cleaned_data['title']

        if "ไอทีหมีแพนด้า" not in data:
            raise forms.ValidationError("คุณลืมชื่อคณะ")
        return data

    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get('start_date')
        end = cleaned_data.get('end_date')

        if start and not end:
            raise forms.ValidationError('โปรดเลือกวันที่สิ้นสุด')
        elif end and not start:
            raise forms.ValidationError('โปรดเลือกวันที่เริ่มต้น')


class CommentForm(forms.Form):
    title = forms.CharField(max_length=100)
    body = forms.CharField(max_length=500, widget=forms.Textarea)
    email = forms.EmailField(required=False)
    tel = forms.CharField(max_length=10, required=False)

    def clean_tel(self):
        data = self.cleaned_data['tel']

        print(data)

        if len(data) != 10 and data:
            print("hjgjhgjhg")
            self.add_error('tel', 'หมายเลขโทรศัพท์ต้องมี 10 หลัก')
        if data.isalpha() and data:
            print("isAlpha")
            self.add_error('tel', 'หมายเลขโทรศัพท์ต้องเป็นตัวเลขเท่านั้น')
        return data

    def clean_email(self):
        data = self.cleaned_data['email']

        if '@' not in data and data:
            raise forms.ValidationError('Enter Valid Email Address')
        return data

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        tel = cleaned_data.get('tel')

        if not tel and not email:
            raise forms.ValidationError('ต้องกรอก Email หรือ Mobile number')


class ChangePasswordForm(forms.Form):
    old_pass = forms.CharField(label="รหัสผ่านเก่า:", max_length=100, required=True)
    new_pass = forms.CharField(label="รหัสผ่านใหม่:", max_length=100, required=True)
    confirm_pass = forms.CharField(label="ยืนยันรหัสผ่าน:", max_length=100, required=True)

    def clean_new_pass(self):
        data = self.cleaned_data['new_pass']

        if len(data) < 8:
            self.add_error('new_pass', 'รหัสผ่านต้องมีมากกว่า 8 ตัวอักษร')
        return data

    def clean(self):
        clean_data = super().clean()
        new_pass = clean_data.get('new_pass')
        print(new_pass)
        confirm_pass = clean_data.get('confirm_pass')

        if new_pass != confirm_pass:
            print(new_pass)
            print(confirm_pass)
            raise forms.ValidationError('รหัสผ่านใหม่ กับ ยืนยันรหัสผ่านต้องเหมือนกัน')


class QuestionForm(forms.Form):
    question_id = forms.IntegerField(required=False, widget=forms.HiddenInput)
    text = forms.CharField()
    type = forms.ChoiceField(choices=Question.TYPES, initial='01')


class PollModelForm(forms.ModelForm):

    class Meta:
        model = Poll
        exclude = ['del_flag']

    def clean_title(self):
        data = self.cleaned_data['title']

        if "ไอทีหมีแพนด้า" not in data:
            raise forms.ValidationError("คุณลืมชื่อคณะ")
        return data

    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get('start_date')
        end = cleaned_data.get('end_date')

        if start and not end:
            raise forms.ValidationError('โปรดเลือกวันที่สิ้นสุด')
        elif end and not start:
            raise forms.ValidationError('โปรดเลือกวันที่เริ่มต้น')


class ChoiceModelForm(forms.ModelForm):

    class Meta:
        model = Choice
        fields = '__all__'
        





