import os
import django
import random
from faker import Faker

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AgroBackEnd.settings')
django.setup()

from submissions.models import StoredDiagnosis

fake = Faker()

# Common plant names
PLANTS = [
    'Tomato', 'Corn', 'Wheat', 'Rice', 'Soybean', 'Potato', 'Apple', 'Banana',
    'Grape', 'Strawberry', 'Blueberry', 'Pepper', 'Cucumber', 'Lettuce', 'Carrot',
    'Onion', 'Garlic', 'Pea', 'Bean', 'Spinach', 'Cabbage', 'Broccoli', 'Cauliflower',
    'Pumpkin', 'Watermelon', 'Melon', 'Eggplant', 'Okra', 'Sunflower', 'Cotton',
    'Coffee', 'Tea', 'Cocoa', 'Pineapple', 'Mango', 'Avocado', 'Papaya', 'Peach',
    'Pear', 'Plum', 'Cherry', 'Almond', 'Walnut', 'Pecan', 'Cashew', 'Pistachio',
    'Oat', 'Barley', 'Rye', 'Sorghum', 'Millet', 'Cassava', 'Sweetpotato', 'Yam',
    'Taro', 'Plantain', 'Coconut', 'Olive', 'Sugarcane', 'Tobacco', 'Rubber',
    'Palm', 'Flax', 'Hemp', 'Jute', 'Kenaf', 'Sisal', 'Bamboo', 'Eucalyptus',
    'Pine', 'Oak', 'Maple', 'Birch', 'Willow', 'Poplar', 'Redwood', 'Sequoia',
    'Cedar', 'Fir', 'Spruce', 'Hemlock', 'Larch', 'Juniper', 'Cypress', 'Yew',
    'Magnolia', 'Dogwood', 'Redbud', 'Hawthorn', 'Holly', 'Azalea', 'Rhododendron',
    'Camellia', 'Gardenia', 'Jasmine', 'Lavender', 'Rosemary', 'Sage', 'Thyme',
    'Basil', 'Oregano', 'Mint', 'Parsley', 'Dill', 'Cilantro', 'Chive', 'Lemongrass',
    'Ginger', 'Turmeric', 'Vanilla', 'Cinnamon', 'Nutmeg', 'Clove', 'Peppercorn',
    'Cardamom', 'Fennel', 'Cumin', 'Coriander', 'Mustard', 'Saffron', 'Anise',
    'Marjoram', 'Tarragon', 'Bay', 'Chervil', 'Savory', 'Stevia', 'Horehound',
    'Hyssop', 'Lovage', 'Borage', 'Chamomile', 'Echinacea', 'Feverfew', 'Lemonbalm',
    'Mullein', 'Pennyroyal', 'Rue', 'Tansy', 'Vervain', 'Yarrow', 'Arnica',
    'Calendula', 'Comfrey', 'Dandelion', 'Plantain', 'Stjohnswort', 'Valerian',
    'Witchhazel', 'Aloe', 'Agave', 'Yucca', 'Cactus', 'Orchid', 'Lily', 'Tulip',
    'Daffodil', 'Hyacinth', 'Iris', 'Dahlia', 'Peony', 'Rose', 'Carnation',
    'Chrysanthemum', 'Aster', 'Daisy', 'Marigold', 'Zinnia', 'Petunia', 'Begonia',
    'Geranium', 'Impatiens', 'Pansy', 'Violet', 'Foxglove', 'Lupine', 'Poppy',
    'Snapdragon', 'Sweetpea', 'Columbine', 'Delphinium', 'Hollyhock', 'Larkspur'
]

# Disease templates with placeholders for plant names
DISEASE_TEMPLATES = [
    {
        "title": "{plant} Powdery Mildew",
        "condition": "The {plant} plant is suffering from a fungal infection causing white powdery growth on leaves.",
        "cause": "Caused by fungal pathogens in the Erysiphales order. Spread through spores in humid conditions.",
        "signs": "White powdery spots primarily on upper leaf surfaces, yellowing leaves, distorted or stunted growth.",
        "controls": "Apply sulfur or potassium bicarbonate-based fungicides. Improve air circulation around {plant} plants. Remove severely infected leaves.",
        "summary": "Fungal disease affecting {plant} leaves, manageable with proper cultural practices and fungicides."
    },
    {
        "title": "{plant} Leaf Spot Disease",
        "condition": "The {plant} plant shows signs of bacterial/fungal leaf spot infection.",
        "cause": "Caused by various fungi (e.g., Cercospora, Septoria) or bacteria (e.g., Xanthomonas). Spread by water splash.",
        "signs": "Circular brown/black spots with yellow halos on leaves, spots may coalesce, premature leaf drop.",
        "controls": "Remove infected leaves. Avoid overhead watering. Apply copper-based fungicides/bactericides for {plant}.",
        "summary": "Common foliar disease of {plant} causing spotting and defoliation, requiring sanitation and protective sprays."
    },
    {
        "title": "{plant} Root Rot",
        "condition": "The {plant} plant is experiencing root system deterioration.",
        "cause": "Caused by overwatering, poor drainage, or soil-borne pathogens like Phytophthora, Fusarium, or Pythium.",
        "signs": "Wilting despite adequate water, yellowing lower leaves, stunted growth, black/brown mushy roots.",
        "controls": "Improve soil drainage for {plant}. Reduce watering frequency. Apply fungicide drenches if fungal cause is confirmed.",
        "summary": "Serious condition of {plant} where roots decay, often fatal if not addressed early with cultural changes."
    },
    {
        "title": "{plant} Aphid Infestation",
        "condition": "The {plant} plant is under attack by sap-sucking aphids.",
        "cause": "Soft-bodied insects (Aphidoidea) feeding on plant sap, often introduced by ants or wind dispersal.",
        "signs": "Clusters of small insects on new growth, sticky honeydew secretion, sooty mold growth, leaf curling.",
        "controls": "Spray {plant} with insecticidal soap or neem oil. Introduce ladybugs/lacewings. Control ant populations.",
        "summary": "Aphids damaging {plant} by feeding on sap, controllable with integrated pest management approaches."
    },
    {
        "title": "{plant} Blossom End Rot",
        "condition": "The {plant} plant shows physiological disorder affecting fruit development.",
        "cause": "Calcium deficiency combined with irregular water uptake, not caused by pathogens.",
        "signs": "Dark, sunken leathery patches on fruit blossom ends, most common in young developing fruits of {plant}.",
        "controls": "Maintain consistent soil moisture for {plant}. Apply calcium supplements if soil tests indicate deficiency.",
        "summary": "Non-pathogenic disorder of {plant} fruits related to calcium metabolism and water relations."
    },
    {
        "title": "{plant} Bacterial Wilt",
        "condition": "The {plant} plant is infected with a systemic bacterial disease.",
        "cause": "Caused by Ralstonia solanacearum bacterium, spread through contaminated soil, water, or tools.",
        "signs": "Rapid wilting of {plant} despite moist soil, brown discoloration of vascular tissue, plant collapse.",
        "controls": "Remove and destroy infected {plant} plants. Rotate with non-host crops. Use disease-free planting material.",
        "summary": "Devastating bacterial disease of {plant} causing sudden wilting and plant death, difficult to control."
    },
    {
        "title": "{plant} Mosaic Virus",
        "condition": "The {plant} plant shows symptoms of viral infection.",
        "cause": "Various viruses (e.g., TMV, CMV) transmitted by insects, tools, or infected plant material.",
        "signs": "Mottled light/dark green patterns on {plant} leaves, leaf distortion, stunted growth, reduced yield.",
        "controls": "Remove infected {plant} plants. Control aphid vectors. Disinfect tools. Use virus-resistant varieties.",
        "summary": "Viral disease causing characteristic mosaic patterns on {plant} leaves, managed through prevention."
    },
    {
        "title": "{plant} Rust Disease",
        "condition": "The {plant} plant is infected with a fungal rust pathogen.",
        "cause": "Rust fungi (Pucciniales) requiring moisture for spore germination and infection.",
        "signs": "Small rust-colored pustules on {plant} leaves/stems, yellow halos around pustules, premature defoliation.",
        "controls": "Apply fungicides labeled for rust on {plant}. Space plants for air circulation. Remove infected debris.",
        "summary": "Fungal disease causing rusty pustules on {plant}, requiring fungicide applications for control."
    },
    {
        "title": "{plant} Nutrient Deficiency",
        "condition": "The {plant} plant shows signs of nutritional imbalance.",
        "cause": "Inadequate soil nutrients, improper pH, or root damage impairing nutrient uptake.",
        "signs": "Varies by nutrient: yellowing (N), purple tint (P), edge burn (K), interveinal chlorosis (Mg,Fe) on {plant}.",
        "controls": "Conduct soil test for {plant}. Apply balanced fertilizer. Adjust pH if needed. Foliar feed for quick correction.",
        "summary": "Nutritional disorder of {plant} correctable through proper fertilization and soil management."
    },
    {
        "title": "{plant} Sunscald",
        "condition": "The {plant} plant shows damage from excessive sunlight exposure.",
        "cause": "Sudden exposure to intense sunlight after cloudy periods or improper hardening off of {plant}.",
        "signs": "White or bleached patches on {plant} leaves/fruits, tissue becomes papery, may crack or shrivel.",
        "controls": "Acclimate {plant} gradually to sun. Provide shade during hottest hours. Maintain adequate watering.",
        "summary": "Environmental damage to {plant} from excessive sunlight, preventable with proper acclimation."
    }
]

def create_diagnoses():
    # Ensure we don't duplicate plant names
    random.shuffle(PLANTS)
    plants_to_use = PLANTS[:200] if len(PLANTS) >= 200 else PLANTS * (200 // len(PLANTS)) + PLANTS[:200 % len(PLANTS)]
    
    for i, plant in enumerate(plants_to_use):
        template = random.choice(DISEASE_TEMPLATES)
        
        diagnosis = StoredDiagnosis(
            name=plant,
            diagnosis_title=template["title"].format(plant=plant),
            health_condition=template["condition"].format(plant=plant),
            cause=template["cause"],
            disease_signs=template["signs"],
            control_suggestions=template["controls"].format(plant=plant),
            summary=template["summary"].format(plant=plant)
        )
        diagnosis.save()
        
        print(f"Created diagnosis {i+1}/200: {diagnosis.diagnosis_title}")

if __name__ == '__main__':
    print("Starting to populate diagnoses...")
    create_diagnoses()
    print("Successfully populated 200 plant diagnoses!")