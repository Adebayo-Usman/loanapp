#Importing required libraries --------------------------------------> step 1
import numpy as np   # => convert user input data to a NumPy array
import pickle        # => use to load trained model
import streamlit as st   # => use to build the web app

#Loading trained model ------------------------------------------------> step 2
load_model = pickle.load(open('lr_model.sav', 'rb'))

#Prediction function  -----------------------------------------------------------> step 3
def loan_prediction(input_data):

    #converting input_data to a numpy array
    input_array = np.array(input_data).reshape(1,-1)

    prediction =  load_model.predict(input_array)

    #conditional statement for prediction
    if prediction =='0':
        return 'Sorry you are not eligible to loan'
    else:
        return 'Congratulations you are eligible to loan'


#creating streamlit interface --------------------------------------------------------------------> step 4
def main():
    st.title('Loan Prediction App') #web app header
    col1, col2, col3 = st.columns(3)

    #--------------------------Column 1(Gender	Married	Dependents	Education, Self_Employed)
    with col1:
        Gender = st.selectbox('Gender', options=['Male','Female'])
        Married = st.selectbox('Married', options=['Yes','No'])
        Dependents = st.selectbox('Dependents', options=['0','1','2','3+'])
        Education = st.selectbox('Education', options=['Graduate','Non-Graduate'])

    #--------------------------Column 2(Self_Employed ApplicantIncome	CoapplicantIncome	LoanAmount)
    with col2:
        Self_Employed = st.selectbox('Self_Employed', options=['Yes','No'])
        applicantincome	= st.number_input('ApplicantIncome', min_value=0, value=0)
        coapplicantincome	= st.number_input('CoapplicantIncome', min_value=0, value=0)
        loanamount	= st.number_input('LoanAmount', min_value=0, value=0)

    #--------------------------Column 3(Loan_Amount_Term Credit_History	Property_Area)
    with col3:
        loanamountterm = st.number_input('Loan_Amount_Term (Days)', min_value=0, max_value=360, step=1)
        Credit_History = st.selectbox('Credit_History',options=['1 (Good)','0 (Bad)'])
        Property_Area = st.selectbox('Property_Area', options=['Rural', 'Semiurban', 'Urban'])

#setup a prediction button ---------------------------------------------------------------------------------> step 5
    if st.button('Bank loan Application'):
        try:
            gender = 1 if Gender=='Male' else 0
            married = 1 if Married=='Yes' else 0
            dependents = 3 if Dependents=='3+' else int(Dependents)
            education = 1 if Education=='Graduate' else 0
            self_employed = 1 if Self_Employed=='Yes' else 0
            credit_history = (1 if Credit_History.startswith('1') else 0)
            rural = 1 if Property_Area=='Rural' else 0
            semiurban = 1 if Property_Area=='Semiurban' else 0
            urban = 1 if Property_Area=='Urban' else 0

            input_data = [gender, married, dependents, education, self_employed, credit_history, rural, semiurban, urban,applicantincome, coapplicantincome, loanamount,loanamountterm]

            result = loan_prediction(input_data)

            if 'Approved' in result:
                st.sucess(result)
            else:
                st.error(result)

        except ValueError as ve:
            st.error(f'Value Error (Check your features) {ve}')


#Run App ---------------------------------------------------------------------------------> step 6
if __name__ == '__main__':
    main()

