# Overview

Put your design documentation in this folder.
This should include rough notes from the familiarization phase.

Include the following in week1:

## Persona

Write a brief persona of your user using design thinking. Use the following template:

- **Name**: [Name of the user]
- **Age**: [Age of the user]
- **Occupation**: [Occupation of the user]
- **Location**: [Location of the user]
- **Goals**: [Goals of the user]
- **Frustrations**: [Frustrations of the user]
- **Motivations**: [Motivations of the user]
- **Technology**: [Technology used by the user]
- **Experience**: [Experience of the user]
- **Personality**: [Personality of the user]
- **Interests**: [Interests of the user]

Notice: This project focuses on assistive technology for people with disabilities. It is important to treat the topic with respect and sensitivity.

Consider:

- People are not defined by their disabilities.
- People with disabilities are not a homogeneous group.

Your persona should reflect the diversity of people with disabilities and their experiences.

## User Journey

What is the user journey? What are the steps the user takes to achieve their goals?

- **Step 1**: [Description of the step]
- **Step 2**: [Description of the step]
- **Step 3**: [Description of the step]
- **Step 4**: [Description of the step]

## UI Interaction Patterns

What are the UI interaction patterns you will use in your project?
- Use semantic native HTML controls and ARIA roles whenever possible to ensure screen readers understand the structure and role of each element.
- Add Landmark Navigation to help users jump directly to major sections using screen reader shortcuts. For example, a banner would be using a
`header` tag, navigation using `nav` tag, and main content using `main` tag etc.
- Add Structured Headings to allow users to quickly navigate by heading level using their screen reader shortcuts.
- Implement Keyboard-First Navigation by making every interactive element reachable by Tab and usable via keyboard.
- Add Announcements for dynamic content using `aria-live` or polite announcements when content updates without a page reload.
- Implement a collapsible section pattern or list navigation to organise large content such as timestamps, code blocks, and explanation.
- Implement audio cues with text equivalents.
- Implement a search bar to allow users to quickly jump to timestamps and bookmarks.

## AI Prompts

Write down any AI prompts you came up with after your first session

1. Expanding and developing your empathy and understanding of the user
> What challenges do people with total blindness would have when learning how to code? For example, they are watching a youtube tutorial that teaches them coding concepts.

2. Identifying technologies that could be relevant to the problem
> I need to create a full-stack web application that caters to blind users that will enable them to learn from video coding tutorials more effectively. The goal of this project is to improve the accessibility for them. I will be using Django for the backend. What are the other technologies that are relevant to my project?

3. Creating a working prototype.
> Help me create a working prototype of this (AI had context of the project so this prompt was straight forward.)

## Technology Stack

What technologies are you thinking about using

- Django + Django REST Framework (Backend)
- SvelteKit, TailwindCSS (Frontend)
- SQLite / PostgreSQL (Database)
