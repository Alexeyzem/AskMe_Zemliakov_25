from django.core.management.base import BaseCommand, CommandError
from app import models
from faker import Faker
import random

from app.models import Question, Answer


class Counter:
    QUESTION = 0
    USER = 0
    ANSWER = 0
    TAG = 0
    LIKES = 0

    def data_count(self, ratio):
        self.QUESTION = ratio * 10
        self.USER = ratio
        self.ANSWER = ratio * 100
        self.TAG = ratio
        self.LIKES = ratio * 200


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            '-r',
            '--ratio',
            nargs=1,
            default=1,
            type=int,
            help='ratio that be used in fill db',
        )
    def handle(self, *args, **options):
        ratio = options['ratio'][0]
        if ratio < 1:
            return "ratio must be greater than 0"
        count = Counter()
        count.data_count(ratio)

        models.QuestionLike.objects.all().delete()
        models.AnswerLike.objects.all().delete()
        models.Tag.objects.all().delete()
        models.Question.objects.all().delete()
        models.Answer.objects.all().delete()
        models.Profile.objects.all().delete()
        models.User.objects.all().delete()

        print("db filling start")
        fake = Faker()
        tags = []
        used_tags = set()
        for i in range(count.TAG):
            while True:
                tag = fake.word() + f'{i}'
                if tag not in used_tags:
                    used_tags.add(tag)
                    break
            tags.append(models.Tag(title=tag))
        models.Tag.objects.bulk_create(tags)
        print("Tags created successfully")

        users = []
        used_users = set()
        for i in range(count.USER):
            while True:
                user_name = fake.user_name()
                if user_name not in used_users:
                    used_users.add(user_name)
                    break
            users.append(models.User(username=user_name, password=fake.password(), email=fake.email()))
        models.User.objects.bulk_create(users)
        profiles = [models.Profile(rating=random.randint(0,1000), user=users[i], avatar="static/img/img.jpg") for i in range(count.USER)]
        models.Profile.objects.bulk_create(profiles)
        print("Profile created successfully")

        questions =[models.Question(title=fake.word()+f'{i%10}',
                                                text=fake.text(),
                                                author=profiles[random.randint(0,count.USER-1)],
                                                rating=0,
                                                answers_count=0,
                                                created_at=fake.date(),
                                                updated_at=fake.date()) for i in range(count.QUESTION)]

        print("Questions created successfully")

        answers = []
        for _ in range(count.ANSWER):
            question = questions[random.randint(0, count.QUESTION - 1)]
            question.answers_count += 1
            answers.append(models.Answer(text=fake.text(),
                                         author=profiles[random.randint(0, count.USER - 1)],
                                         rating=0,
                                         question=question,
                                         created_at=fake.date(),
                                         updated_at=fake.date()))

        print("Answer created successfully")

        answers_likes = []
        for _ in range(count.LIKES // 2):
            author = profiles[random.randint(0, count.USER - 1)]
            answer = answers[random.randint(0, count.ANSWER - 1)]
            answer.rating += 1
            answers_likes.append(models.AnswerLike(author=author, answer=answer))
        print("Answers likes created successfully")

        question_likes = []
        for _ in range(count.LIKES // 2):
            author = profiles[random.randint(0, count.USER - 1)]
            question = questions[random.randint(0, count.QUESTION - 1)]
            question.rating += 1
            question_likes.append(models.QuestionLike(author=author, question=question))
        models.Question.objects.bulk_create(questions)
        models.QuestionLike.objects.bulk_create(question_likes)
        models.Answer.objects.bulk_create(answers)
        models.AnswerLike.objects.bulk_create(answers_likes)
        print("Questions likes created successfully and all in database successfully")


        for i in range(count.TAG):
            for _ in range(random.randint(1, 20)):
                j = random.randint(0, count.QUESTION-1)
                if questions[j].tags.all().count() < 3:
                    tags[i].question_set.add(questions[j])
        print("Questions with tag created successfully")
        return "Data base filled successfully"
