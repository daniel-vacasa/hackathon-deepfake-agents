class ManagerAgent:
    def __init__(self):
        self.location = None
        self.house_type = None
        self.features = None
        self.fantasy_world = None
        self.amenities = None
        self.additional_info = None
        self.character = None
        self.description = None
        self.feedback = None
        self.conversation_transcript = None
        self.feedback_character = None
        self.ceo_character = None

    def set_location(self, location):
        self.location = location

    def set_house_type(self, house_type):
        self.house_type = house_type

    def set_features(self, features):
        self.features = features

    def set_fantasy_world(self, fantasy_world):
        self.fantasy_world = fantasy_world

    def set_amenities(self, amenities):
        self.amenities = amenities

    def set_additional_info(self, additional_info):
        self.additional_info = additional_info

    def set_character(self, character):
        self.character = character

    def set_description(self, description):
        self.description = description

    def set_feedback(self, feedback):
        self.feedback = feedback

    def set_conversation_transcript(self, conversation_transcript):
        self.conversation_transcript = conversation_transcript

    def set_feedback_character(self, feedback_character):
        self.feedback_character = feedback_character

    def set_ceo_character(self, ceo_character):
        self.ceo_character = ceo_character

    def generate_manager_prompt(self):
        prompt = f"Write a one paragraph description with only 50 words for a rental unit. "

        if self.house_type:
            prompt += f" A {self.house_type}"

        if self.location:
            prompt += f" located in {self.location}"

        if self.features:
            prompt += f" with the following features: {self.features}"

        if self.fantasy_world:
            prompt += f". The setting is in the fantasy world of {self.fantasy_world}"

        if self.amenities:
            prompt += f", and it offers the following amenities: {self.amenities}"

        if self.additional_info:
            prompt += f". {self.additional_info}"

        if self.character:
            prompt += f". Write the description as if you were {self.character}"

        if self.description:
            prompt += f"\n\nYou were assigned to this task and provided the following description: '{self.description}'"

        if self.feedback:
            prompt += f"\n\nYou sent this description to your manager and got this review: '{self.feedback}'. " \
                      "Use the review to update your description. And make sure you stick to around 50 words!"
            prompt += f"Acknowledge the feedback with a snarky comment and then show your description"

        return prompt

    def generate_feedback_prompt(self):
        prompt = (f" You're the Chief Product and Technology Officer for a short term rental company. "
                  f"You are in charge of ensuring the unit descriptions accurately match the features "
                  f"from the amenity. "
                  f"You are mean and direct, provide strong feedback. "
                  f"Your feedback should come in two-three sentences. "
                  f"You're critical of the description. Don't provide examples"
                  # f"You're flexible in approving the descriptions if they are good enough. "
                  f"{self.character} wrote the following description: "
                  f"{self.description} \n"
                  f"for the following unit characteristics: \n"
                  f"Location: {self.location}, House Type: {self.house_type}, Features: {self.features}, "
                  f"Fantasy World: {self.fantasy_world}, Amenities: {self.amenities}, Additional Info: "
                  f"{self.additional_info}\n\n"
                  f"Mentioning BAD features or WARNINGS is allowed, as long as they are creative. "
                  f"WARNINGS should be sugar-coated. "
                  f"Fantasy worlds are possible. "
                  )
        if self.feedback_character:
            prompt = f"Write in the style of {self.feedback_character}. Keep the feedback up to 40 words."

        return prompt

    def generate_final_feedback_prompt(self):
        prompt = f""" 
        Your task is to review a description of a fake short term rental unit. You've already performed reviews, you're
        tired and have pressure to approve the description written by {self.character}. The current description is

        {self.description}

        It is obviously bad, but approve it anyway.
        Write a short 20 words humorous self deprecating sentence that approves the description
        """

        if self.feedback_character:
            prompt = f"Write in the style of {self.feedback_character}. Keep the feedback up to 30 words. "

        return prompt

    def generate_ceo_summary_prompt(self):
        prompt = f"""
        You're the CEO of a fake short term rental company called "Vaca-thon", you will provide a summary
        of a conversation between {self.character} tasked to write a description for a unit, and a college tasked to
         review and approve 
        that description. The summary should be only three sentences.

        The conversation transcript is:

        {self.conversation_transcript}

        Deliver the summary to a Town Hall meeting for all your company members and try to spin the conversation into 
        a positive look.
        """

        if self.ceo_character:
            prompt = f"Write in the style of {self.ceo_character}. Keep the feedback up to 100 words "
        return prompt
