import streamlit as st
import numpy as np
import pandas as pd
import folium
from streamlit_folium import st_folium
import plotly.graph_objects as go
import plotly.express as px


APP_TITLE = 'CSC 47400 Project 1 - Khanh Huang'
APP_SUB_TITLE = 'COVID-19 Vaccination Dashboard'

def display_char(df):

    total_vaccinated = df['Population Vaccinated'].sum()
    total_population = df['TOTAL Population'].sum()
    total_vaccination_rate = total_vaccinated / total_population

    # Create a bar chart that shows the vaccination rate by region
    fig1 = px.bar(df, x='WHO_REGION', y='% Population vaccinated',hover_name='COUNTRY', color='WHO_REGION')
    fig1.update_layout(title='Vaccination Rate by Region')

    # Create a scatter plot that shows the relationship between population and vaccination rate
    fig2 = px.scatter(df, x='TOTAL Population', y='% Population vaccinated', hover_name='COUNTRY', log_x=True)
    fig2.update_layout(title='Population vs Vaccination Rate')


    st.markdown(f'Total number of people vaccinated: **{total_vaccinated:,.0f}**')
    st.markdown(f'Total population: **{total_population:,.0f}**')
    st.markdown(f'Total vaccination rate: **{total_vaccination_rate:.2%}**')

    st.plotly_chart(fig1)
    st.plotly_chart(fig2)

def display_map(df):

    map = folium.Map(location = [38,100],zoom_start=1,scrollWheelZoom=False)

    choropleth = folium.Choropleth(
        geo_data = 'countries.geojson',
        data = df,
        columns=('ISO3','% Population vaccinated'),
        key_on = 'feature.properties.ISO_A3',

        highlight=True
    )
    choropleth.geojson.add_to(map)

    df = df.set_index('ISO3')
    iso_name = 'AFG'
    from datetime import datetime
    for feature in choropleth.geojson.data['features']:
        iso_name = feature['properties']['ISO_A3']
        feature['properties']['population'] = 'Population: ' +  str('{:,}'.format(round(df.loc[iso_name,'TOTAL Population'])) if iso_name in list(df.index) else 'N/A')

        feature['properties']['date'] = 'Date updated: ' + str(df.loc[iso_name, 'DATE_UPDATED'].strftime("%b %d, %Y") if iso_name in list(df.index) else 'N/A')
        feature['properties']['num_vaccine_used'] = 'Number of vaccine types used: ' + str(df.loc[iso_name, 'NUMBER_VACCINES_TYPES_USED'].astype(int) if iso_name in list(df.index) else 'N/A')
        feature['properties']['protect_orginal_serve'] = 'Percent people protected for Orginal serve: ' +  str('{:,}'.format(round(df.loc[iso_name,'% People Protected for ORGINAL SEVERE'])) if iso_name in list(df.index) else 'N/A')
        feature['properties']['protect_orginal_infec'] = 'Percent people protected for Orginal infection: ' +  str('{:,}'.format(round(df.loc[iso_name,'% People Protected for ORGINAL INFECTION'])) if iso_name in list(df.index) else 'N/A')
        feature['properties']['protect_omicron_serve'] = 'Percent people protected for OMICRON serve: ' +  str('{:,}'.format(round(df.loc[iso_name,'% People Protected for OMICRON SEVERE'])) if iso_name in list(df.index) else 'N/A')
        feature['properties']['protect_omicron_infec'] = 'Percent people protected for OMICRON infection: ' +  str('{:,}'.format(round(df.loc[iso_name,'% People Protected for OMICRON INFECTION'])) if iso_name in list(df.index) else 'N/A')
        feature['properties']['sucep_orginal_serve'] = 'Percent suceptible for breakhrough Orginal serve: ' +  str('{:,}'.format(round(df.loc[iso_name,'% SUCEPTIBLE for  BREAKTHROUGH  ORGINAL SEVERE'])) if iso_name in list(df.index) else 'N/A')
        feature['properties']['sucep_orginal_infec'] = 'Percent suceptible for breakhrough Orginal infection: ' +  str('{:,}'.format(round(df.loc[iso_name,'% SUCEPTIBLE for  BREAKTHROUGH ORIGINAL  INFECTION'])) if iso_name in list(df.index) else 'N/A')
        feature['properties']['sucep_omicron_serve'] = 'Percent suceptible for breakhrough OMICRON serve: ' +  str('{:,}'.format(round(df.loc[iso_name,'% SUCEPTIBLE for  BREAKTHROUGH OMICRON SEVERE'])) if iso_name in list(df.index) else 'N/A')
        feature['properties']['sucep_omicron_infec'] = 'Percent suceptible for breakhrough OMICRON infection: ' +  str('{:,}'.format(round(df.loc[iso_name,'% SUCEPTIBLE for  BREAKTHROUGH OMICRON INFECTION'])) if iso_name in list(df.index) else 'N/A')
        feature['properties']['percent_not_vac'] = 'Percent Population not vaccinated: ' +  str('{:,}'.format(round(df.loc[iso_name,'% Population NOT VACCINATED'])) if iso_name in list(df.index) else 'N/A')



    choropleth.geojson.add_child(
        folium.features.GeoJsonTooltip(['ADMIN','population','date','num_vaccine_used','percent_not_vac','protect_orginal_serve','sucep_orginal_serve','protect_orginal_infec','sucep_orginal_infec','protect_omicron_serve','sucep_omicron_serve','protect_omicron_infec','sucep_omicron_infec'], labels = False)
    )

    st_map = st_folium(map,width = 1000, height = 450)
    country_name =''
    if st_map['last_active_drawing']:
       country_name = st.write(st_map['last_active_drawing']['properties']['ADMIN'])
    return country_name

def display_info(df,country_name,info,metric_title):
    df = df[(df['COUNTRY'] == country_name)]
    if country_name:
        df = df[df['COUNTRY'] == country_name]
    df.drop_duplicates(inplace = True)
    total  = df[info].sum()
    st.metric(metric_title,'{:,}'.format(total))


def main():
    st.set_page_config(APP_TITLE)
    st.title(APP_TITLE)
    st.caption(APP_SUB_TITLE)

    # Load Excel file into Pandas dataframe
    df = pd.read_excel('data.xlsx',sheet_name='FINAL DATASET FOR VIZ')

    display_char(df)

    country_name = display_map(df)



if __name__ =="__main__":
    main()
