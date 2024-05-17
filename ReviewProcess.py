import Roles
# %run
# Roles.ipynb

manager = Roles.ManagerAgent()

# Any of this attributes can change
manager.set_location("Los Angeles")
manager.set_features("Near a taco shop")
manager.set_house_type("")
manager.set_fantasy_world("Earth")
manager.set_amenities("cute sleeping bag")
manager.set_additional_info("No homeless people nearby")

# Set of characters
manager.set_character("Kim Kardashian")         # Writes the description
manager.set_feedback_character("Kanye West")    # Reviews and gives feedback
manager.set_ceo_character("Donald Trump")       # Summarizes the generation process

conversation_transcript = []
feedback_count = 0
while feedback_count < 2:

    manager_prompt = manager.generate_manager_prompt()
    character_description = client.evaluate_prompt(prompt=manager_prompt, temperature=0.9).content.replace(r'\r\n',
                                                                                                           '\n')
    manager.set_description(character_description)
    conversation_transcript.append(character_description)
    print(f"{manager.character} writes the following description:")
    print(character_description)
    print("")

    if feedback_count < 1:
        feedback_prompt = manager.generate_feedback_prompt()
        feedback = client.evaluate_prompt(prompt=feedback_prompt, temperature=0.1).content.replace(r'\r\n', '\n')
        manager.set_feedback(feedback)
        conversation_transcript.append(feedback)
        print(f"{manager.feedback_character} gives the following feedback: ")
        print(feedback)
        print("")

    else:
        final_feedback_prompt = manager.generate_final_feedback_prompt()
        feedback = client.evaluate_prompt(prompt=final_feedback_prompt, temperature=0.5).content.replace(r'\r\n', '\n')
        conversation_transcript.append(feedback)
        print(f"{manager.feedback_character} finally said: ")
        print(feedback)
        print("")

    feedback_count += 1

manager.set_conversation_transcript(conversation_transcript)
summary_of_conversation_prompt = manager.generate_ceo_summary_prompt()
CEO_summary = client.evaluate_prompt(prompt=summary_of_conversation_prompt, temperature=0.1).content.replace(r'\r\n',
                                                                                                             '\n')
print("The CEO returned: ")
print(CEO_summary)
print("")
