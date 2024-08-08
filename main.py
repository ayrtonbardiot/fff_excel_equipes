import requests
import xlsxwriter
import string

championnat = 423913 # r2 cvdl
poule = 1 # poule A

def get_equipes():
    response = requests.get(f"https://api-dofa.prd-aws.fff.fr/api/engagements.json?competition.cp_no={championnat}&phase.ph_no=1&poule.gp_no={poule}")
    equipes = response.json()
    return equipes

def get_club(cl_no):
    response = requests.get(f"https://api-dofa.prd-aws.fff.fr/api/clubs/{cl_no}.json")
    club = response.json()
    return club

def get_terrain(terrain):
    terrain = terrain.split('/api/terrains/')[1]
    response = requests.get(f"https://api-dofa.prd-aws.fff.fr/api/terrains/{terrain}.json")
    terrain = response.json()
    return terrain

def get_club_logo(affiliation_number):
    response = requests.get(f"https://cdn-transverse.azureedge.net/phlogos/BC{affiliation_number}.jpg")
    with open(f'logos/logo_{affiliation_number}.jpg', 'wb') as f:
        f.write(response.content)

def write_excel(data):
    initcompet = data[0]['equipe']
    workbook = xlsxwriter.Workbook(f'equipes_{initcompet['competition']['name'] + '_' + initcompet['poule']['name'] + '_' + initcompet['competition']['cdg']['name']}.xlsx')
    worksheet = workbook.add_worksheet()
    worksheet.write(0, 0, initcompet['competition']['name'] + ' - ' + initcompet['poule']['name'] + ' - ' + initcompet['competition']['cdg']['name'])
    worksheet.write(1, 0, 'Team ID')
    worksheet.write(1, 1, 'Team Image')
    worksheet.write(1, 2, 'Team Name')
    worksheet.write(1, 3, 'Ground Name')
    worksheet.write(1, 4, 'Ground address')
    worksheet.write(1, 5, 'Ground postal code')
    worksheet.write(1, 6, 'Ground city')
    worksheet.write(1, 7, 'Ground latitude')
    worksheet.write(1, 8, 'Ground longitude')
    for i, value in enumerate(data):
        i += 2
        worksheet.write(i, 0, value['club']['cl_no'])
        worksheet.embed_image(i, 1, f'logos/logo_{value["club"]["affiliation_number"]}.jpg', {'x_offset': 15, 'y_offset': 10, 'x_scale': 0.5, 'y_scale': 0.5})
        worksheet.write(i, 2, value['equipe']['equipe']['short_name'])
        worksheet.write(i, 3, value['terrain']['name'])
        worksheet.write(i, 4, value['terrain']['address'])
        worksheet.write(i, 5, value['terrain']['zip_code'])
        worksheet.write(i, 6, value['terrain']['city'])
        worksheet.write(i, 7, value['terrain']['latitude'])
        worksheet.write(i, 8, value['terrain']['longitude'])

    workbook.close()

def main():
    equipes = get_equipes()
    data = []
    for equipe in equipes:
        club = get_club(equipe['equipe']['club']['cl_no'])
        terrain = get_terrain(equipe['terrain'])
        get_club_logo(club['affiliation_number'])
        data.append({'equipe': equipe, 'club': club, 'terrain': terrain})
    write_excel(data)    

if __name__ == "__main__":
    championnat = input("Entrez l'ID de championnat : ")
    poule_letter = input("Entrez la poule (A, B, ...) : ")
    poule = string.ascii_uppercase.index(poule_letter) + 1
    main()