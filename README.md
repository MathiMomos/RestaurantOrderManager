# Summary of First Deliverable: POS System for "El Criollito" Restaurant

This document outlines the planning and initial analysis of an integrated order management system for the restaurant "El Criollito." The main goal is to optimize operational efficiency and enhance customer experience in a dynamic and competitive restaurant environment.

## 1. Introduction

The project aims to develop a comprehensive system that streamlines all stages of the ordering process, from customer input to final bill issuance. The software will allow diners to interact via a user-friendly interface to customize and send orders directly to the kitchen in real time, reducing errors and improving communication accuracy.

It will also include table and reservation management, automatic bill generation, and dynamic menu administration.

### Team Members (Group 3)

- **Manuel Chumpitazi Ruiz**
- **Gabriel Mathias Davalos Velazco**
- **Fabrizio Huaytalla Llacsahuanga**
- **Kevin Mendoza Chamorro**
- **Andres Fernando Morales Usca**
- **Arley Oscar Sabogal Crisostomo**

## 2. Planning

### Project Purpose

The system will enable customers to efficiently place and customize their orders, send them to the kitchen, and automatically generate a detailed bill. It will integrate orders, kitchen management, and billing to streamline workflows.

### Project Description

The system targets a Peruvian creole cuisine restaurant, with the head chef as the main client. The goal is to enhance communication between customers and kitchen staff.

### Project Objectives

- Improve order taking
- Organize orders by arrival time
- Enhance billing efficiency
- Make order monitoring easier in the kitchen
- Generate a final bill automatically
- Manage table occupancy

### Project Scope

**Included:**

- **Table and Reservation Management**: Real-time availability and assignment
- **Order Management**: Friendly customer interface with real-time kitchen communication
- **Menu Management**: Dynamic updates to dishes, prices, and promotions
- **System Integration**: Fully integrated modules for seamless information flow
- **Order Database**: Efficient tracking (ID, date, time, table number, user)

**Excluded:**

- External accounting/payment platform integrations
- Multi-branch management
- Full financial management modules
- Advanced customer profiling (basic info only)
- Mobile/tablet apps or third-party integration (initial version)
- Long-term tech support and updates beyond the first year

---

### Project Team

- **Project Manager**: Andres Fernando Morales Usca  
- **System Analyst/Designer**: Fabrizio Huaytalla Llacsahuanga  
- **Developers**: Gabriel Mathias Davalos Velazco, Arley Oscar Sabogal Crisostomo  
- **Quality Assurance**: Kevin Mendoza Chamorro  
- **Deployment**: Manuel Chumpitazi Ruiz  

---

### Project Timeline (SCRUM Methodology)

The project will follow a sprint-based SCRUM methodology:

- **Sprint 1 (Sep 8–16)**: Define objectives, gather requirements, plan DB/environment, quality criteria, deployment plan  
- **Sprint 2 (Sep 17–22)**: Design architecture, database structure, initial UI, and test environment  
- **Sprint 3 (Sep 23–30)**: Start development, implement DB, reservation/order modules, functional testing  
- **Sprint 4 (Oct 1–10)**: Improve DB, UI, and perform performance testing  
- **Sprint 5 (Oct 11–25)**: Finalize advanced features (order tracking, menu), integration tests, production prep  
- **Sprint 6 (Oct 26–Nov 3)**: Final design tweaks, system stability, client acceptance tests, and final deployment  

---

### Estimated Budget

The project is estimated to cost **S/.7500 or more**, covering development, testing, and technological resources.

---

## 3. Analysis

### Requirements Gathering Methods

- **Client Interviews**: Meetings with the restaurant owner
- **Textual Specification**: Plain text requirements for analysis
- **Functional Decomposition**: Modular breakdown of system functions

### Functional Requirements

- **Order Creation**: Customer info, dish selection, quantity, review, and submission  
- **Kitchen Management**: Receive and confirm orders, update preparation status  
- **Order Finalization**: Generate and deliver bill, save transaction in DB  
- **User Interfaces**: Friendly customer UI, specialized kitchen/staff interfaces

### Non-Functional Requirements

- **Product**: Usability, scalability, intuitive UI, high availability, minimal failure rate  
- **Organizational**: Data protection compliance, staff training  
- **External**: Multi-browser/device support, compliance with Peruvian law, basic maintenance

---

### Core Business Processes

- **Table Management**: Status verification (active/inactive), automatic assignment  
- **Order Handling**: Customer entry, dish selection, confirmation  
- **Kitchen Notification**: Orders displayed on kitchen screen  
- **Order Preparation**: Status update: "Preparing" → "Ready to Serve"  
- **Payment**: Status view, bill request, payment processing, table status update  
- **Database Logging**: Store all transaction data for future reference

---

### Requirement Analysis Techniques

- **UML Diagrams (Flowcharts, Use Cases)**: Clear process visualization  
- **Visual Prototypes**: UI previews for early validation and feedback  
- **Process Modeling**: Flow diagrams for key system activities  
- **Use Cases**: Step-by-step interaction scenarios between system and users

---

## Tools and Technologies

Below are the primary technologies used in the project:

### 🛠️ Figma – UI/UX Design
![Figma](https://upload.wikimedia.org/wikipedia/commons/3/33/Figma-logo.svg)

### 🗃️ MySQL – Database Management
![MySQL](https://upload.wikimedia.org/wikipedia/en/d/dd/MySQL_logo.svg)

### 📐 UML Diagrams – Visual Modeling (Using Lucidchart/Draw.io)
![UML](https://upload.wikimedia.org/wikipedia/commons/6/6d/UML_logo.svg)

---
