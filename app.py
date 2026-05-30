import streamlit as st
import tensorflow as tf
import numpy as np
import pickle

from PIL import Image
from datetime import datetime
from keras.applications.mobilenet_v2 import preprocess_input


# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="Face Style Studio",
    page_icon="💎",
    layout="wide"
)


# ==================================================
# SESSION
# ==================================================

if "result" not in st.session_state:
    st.session_state.result=None

if "history" not in st.session_state:
    st.session_state.history=[]



# ==================================================
# MODEL
# ==================================================

@st.cache_resource
def load_ai():

    model=tf.keras.models.load_model(
        "face_shape_model.keras"
    )

    with open(
        "encoder.pkl",
        "rb"
    ) as f:
        encoder=pickle.load(f)

    return model,encoder


model,encoder=load_ai()



# ==================================================
# STYLE DATABASE
# ==================================================

STYLE={


"oval":{

"hair":[
"Pompadour",
"Quiff",
"Side Part",
"Textured Crop"
],

"beard":[
"Short Box Beard",
"Light Stubble",
"Corporate Beard"
],

"fashion":[
"Smart Casual",
"Premium Blazer",
"Denim Jacket",
"Polo + Chinos"
],

"glass":[
"Aviator",
"Rectangle Frame",
"Wayfarer"
],

"shoes":[
"White Sneakers",
"Loafers"
],

"tips":[
"Most styles match",
"Maintain balanced volume"
],

"vibe":"Classy Modern"

},



"round":{

"hair":[
"High Fade",
"Spiky Hair",
"Pompadour"
],

"beard":[
"Angular Beard",
"Goatee"
],

"fashion":[
"Dark Jacket",
"Vertical Shirt",
"Structured Blazer"
],

"glass":[
"Rectangle",
"Square Frame"
],

"shoes":[
"Boots",
"Minimal Sneakers"
],

"tips":[
"Add height",
"Avoid round glasses"
],

"vibe":"Sharp Confident"

},



"square":{

"hair":[
"Undercut",
"Buzz Cut",
"Textured Crop"
],

"beard":[
"Full Beard",
"Circle Beard"
],

"fashion":[
"Leather Jacket",
"Formal Shirt",
"Classic Suit"
],

"glass":[
"Round Frame",
"Thin Metal Frame"
],

"shoes":[
"Leather Shoes",
"Chelsea Boots"
],

"tips":[
"Highlight jawline",
"Clean edges"
],

"vibe":"Bold Premium"

},



"diamond":{

"hair":[
"Side Part",
"Layered Cut",
"Fringe"
],

"beard":[
"Short Beard",
"Light Stubble"
],

"fashion":[
"Street Wear",
"Bomber Jacket"
],

"glass":[
"Oval Frame",
"Rimless Glass"
],

"shoes":[
"High Sneakers"
],

"tips":[
"Balance cheekbones"
],

"vibe":"Trendy"

},



"heart":{

"hair":[
"Side Swept",
"Medium Layers"
],

"beard":[
"Heavy Stubble",
"Short Beard"
],

"fashion":[
"Layered Outfit",
"Casual Jacket"
],

"glass":[
"Round Frame",
"Aviator"
],

"shoes":[
"Casual Sneakers"
],

"tips":[
"Balance jaw area"
],

"vibe":"Soft Modern"

},



"oblong":{

"hair":[
"Fringe",
"Medium Volume"
],

"beard":[
"Box Beard"
],

"fashion":[
"Hoodie",
"Relaxed Streetwear"
],

"glass":[
"Large Square Frame"
],

"shoes":[
"Sneakers"
],

"tips":[
"Avoid too much height"
],

"vibe":"Urban"

},



"triangle":{

"hair":[
"Messy Layers",
"Crew Cut"
],

"beard":[
"Light Beard"
],

"fashion":[
"Premium Casual",
"Structured Jacket"
],

"glass":[
"Aviator",
"Clubmaster"
],

"shoes":[
"Premium Sneakers"
],

"tips":[
"Increase forehead balance"
],

"vibe":"Creative"

}

}




SKIN={


"Fair":{

"best":[
"Royal Blue",
"Emerald",
"Burgundy",
"Navy"
],

"avoid":[
"Pale Yellow",
"Too White"
],

"accessory":[
"Silver Watch",
"Black Glasses"
]

},



"Medium":{

"best":[
"Olive",
"Cream",
"Maroon",
"Earth Brown"
],

"avoid":[
"Neon",
"Dull Grey"
],

"accessory":[
"Gold Watch",
"Brown Leather"
]

},



"Dark":{

"best":[
"White",
"Pastel Blue",
"Orange"
],

"avoid":[
"Dark Brown"
],

"accessory":[
"Silver Chain",
"Premium Watch"
]

}

}
# ==================================================
# CSS PREMIUM UI
# ==================================================

st.markdown(
"""
<style>

@import url(
'https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;900&display=swap'
);


*{
font-family:Poppins;
}


header,footer{
visibility:hidden;
}


.stApp{

background:
radial-gradient(circle at top left,#7c3aed55,transparent 35%),
radial-gradient(circle at top right,#06b6d455,transparent 30%),
linear-gradient(135deg,#020617,#050020,#000);

color:white;

}


/* remove default */

.block-container{

padding-top:15px;
max-width:95%;

}


/* TITLE */

.title{

font-size:60px;

font-weight:900;

text-align:center;

letter-spacing:8px;

background:

linear-gradient(
90deg,
#22d3ee,
#8b5cf6,
#ec4899
);

-webkit-background-clip:text;
-webkit-text-fill-color:transparent;

}


.subtitle{

text-align:center;

font-size:18px;

color:#cbd5e1;

margin-bottom:25px;

}



/* CARD */


.card{

background:

linear-gradient(
145deg,
rgba(30,30,80,.95),
rgba(5,10,35,.95)
);

border-radius:25px;

padding:25px;

border:

1px solid rgba(255,255,255,.15);

box-shadow:

0 0 30px rgba(59,130,246,.2);

min-height:170px;

transition:.3s;

}


.card:hover{

transform:translateY(-6px);

box-shadow:

0 0 40px #9333ea;

}



.big{

font-size:34px;

font-weight:900;

}



.face{

font-size:65px;

font-weight:900;

text-align:center;


background:

linear-gradient(
90deg,
#ff00cc,
#38bdf8,
yellow
);


-webkit-background-clip:text;

-webkit-text-fill-color:transparent;

}



.green{

color:#22c55e;

}



.grid4{

display:grid;

grid-template-columns:

repeat(4,1fr);

gap:25px;

}



.grid3{

display:grid;

grid-template-columns:

repeat(3,1fr);

gap:25px;

}



.item{

font-size:22px;

line-height:40px;

}



.banner{

margin-top:30px;

padding:30px;

border-radius:25px;

font-size:25px;

background:

linear-gradient(
90deg,
#7c3aed,
#db2777
);

}


</style>
""",
unsafe_allow_html=True
)




# ==================================================
# HEADER
# ==================================================

st.markdown(
"""
<div class="title">

Face Style Studio

</div>

<div class="subtitle">

Face Shape • Fashion • Beard • Hairstyle • Skin Tone Assistant 🚀

</div>

""",
unsafe_allow_html=True
)




# ==================================================
# TOP CARDS
# ==================================================

st.markdown(
"""

<div class="grid4">


<div class="card">

⚡ Speed

<div class="big">

FAST

</div>

Super Quick

</div>


<div class="card">

🎯 Accuracy

<div class="big">

AI

</div>

Smart Prediction

</div>


<div class="card">

🧠 Model

<div class="big">

CNN

</div>

Deep Learning

</div>


<div class="card">

☁ Upload

<div class="big">

IMAGE

</div>

Secure

</div>


</div>

""",
unsafe_allow_html=True
)



st.write("---")



# ==================================================
# INPUT
# ==================================================

c1,c2=st.columns([2,1])


with c1:

    upload=st.file_uploader(
    "☁ Upload Face Image",
    ["jpg","jpeg","png"]
    )


with c2:

    skin=st.selectbox(
    "🎨 Skin Tone",
    list(SKIN.keys())
    )





# ==================================================
# ANALYZE
# ==================================================

if upload:


    image=Image.open(upload).convert("RGB")


    if st.button(
    "✨ Analyze My Style"
    ):


        img=image.resize((224,224))


        arr=np.expand_dims(
        np.array(img),
        axis=0
        )


        arr=preprocess_input(arr)



        pred=model.predict(arr)



        face=encoder.inverse_transform(
        [np.argmax(pred)]
        )[0].lower()



        confidence=float(
        np.max(pred)*100
        )



        st.session_state.result={

        "face":face,

        "confidence":confidence,

        "skin":skin

        }



        st.session_state.history.append(
        st.session_state.result
        )





# ==================================================
# SHOW RESULT
# ==================================================

if st.session_state.result:


    face=st.session_state.result["face"]

    confidence=st.session_state.result["confidence"]

    skin=st.session_state.result["skin"]


    data=STYLE[face]

    skin_data=SKIN[skin]



    a,b,c=st.columns(3)


    with a:

        if upload:

            st.image(
            image,
            use_container_width=True
            )



    with b:


        st.markdown(
        f"""

        <div class="card">

        Detected Face Shape


        <div class="face">

        {face.upper()}

        </div>


        <h3 class="green">

        {confidence:.2f}% Confidence

        </h3>


        ⭐ Style Score

        <h1>

        92/100

        </h1>


        </div>

        """,
        unsafe_allow_html=True
        )




    with c:


        st.markdown(
        f"""

        <div class="card">

        🔥 Style Personality


        <h1>

        {data["vibe"]}

        </h1>


        Skin:

        <h2>

        {skin}

        </h2>


        </div>

        """,
        unsafe_allow_html=True
        )




# ==================================================
# FEATURE CARDS
# ==================================================


    st.markdown(
    f"""

<div class="grid4">


<div class="card item">

👕 Fashion

<br><br>

{"<br>".join(data["fashion"])}

</div>



<div class="card item">

🧔 Beard

<br><br>

{"<br>".join(data["beard"])}

</div>




<div class="card item">

💇 Hairstyle

<br><br>

{"<br>".join(data["hair"])}

</div>




<div class="card item">

👓 Glasses

<br><br>

{"<br>".join(data["glass"])}

</div>


</div>


""",
unsafe_allow_html=True
)




    st.markdown(
    f"""

<div class="grid3">


<div class="card item">

🎨 Best Colors

<br><br>

{"<br>".join(skin_data["best"])}

</div>



<div class="card item">

🚫 Avoid Colors

<br><br>

{"<br>".join(skin_data["avoid"])}

</div>




<div class="card item">

⌚ Accessories

<br><br>

{"<br>".join(skin_data["accessory"])}

</div>


</div>

<br>


<div class="grid3">


<div class="card item">

👞 Shoes

<br><br>

{"<br>".join(data["shoes"])}

</div>



<div class="card item">

💡 Grooming Tips

<br><br>

{"<br>".join(data["tips"])}

</div>



<div class="card item">

🔥 Vibe

<br><br>

{data["vibe"]}

</div>


</div>

""",
unsafe_allow_html=True
)



# ==================================================
# REPORT
# ==================================================

    report=f"""

FACE STYLE STUDIO REPORT

Face Shape:
{face}

Confidence:
{confidence:.2f}%

Skin:
{skin}

Fashion:
{data["fashion"]}

Hair:
{data["hair"]}

Beard:
{data["beard"]}

Glasses:
{data["glass"]}

"""


    st.download_button(

    "📄 Download AI Report",

    report,

    "Face_Report.txt"

    )




# ==================================================
# FOOTER
# ==================================================

st.markdown(
"""

<div class="banner">

👑 Premium AI Fashion Assistant Activated ✨

</div>

""",
unsafe_allow_html=True
)
