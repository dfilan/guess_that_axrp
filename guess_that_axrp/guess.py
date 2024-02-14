import random
import uuid

from flask import Blueprint, render_template, request, session
import markdown

from guess_that_axrp.db import get_db

bp = Blueprint('guess', __name__, url_prefix='/guess')


def pick_random_sentence(text):
    # strip out bolded text
    # turn it into sentences
    split_on_bold = text.split('**')
    # get text after second bolded name (this is a bit hacky) and before final bolded name
    middle_parts = split_on_bold[4:-2]
    middle = '**'.join(middle_parts)
    # split into lines, delete initial bolded names and headers, then re-join
    lines = middle.splitlines()
    lines = list(filter(lambda l: not (l == '' or l.startswith('#') or l.startswith('**')),
                        lines))
    # so: what's a sentence?
    # well a full stop or a question mark demarcates a sentence, as does a newline
    # but we don't want to split on a decimal point (thanks Copilot)
    # (doable by saying it's got to be a space or newline after the full stop or question
    # mark, which also fixes the issue with ellipses)
    # and we also maybe want to preserve quotes
    # oh god sometimes i use a single quotation mark for a long quotation, fuck
    # ok fuck quotations
    sep_period = nice_split(lines, '.')
    sep_bang = nice_split(sep_period, '?')
    # now filter to sentences that are at least 5 words long
    long_sentences = list(filter(lambda sentence: len(sentence.split()) >= 5, sep_bang))
    random_markdown = "> " + random.choice(long_sentences)
    return markdown.markdown(random_markdown)


def nice_split(text_list: list[str], split_char: str) -> list[str]:
    splitter = split_char + ' '
    new_split = []
    for entry in text_list:
        sub_split = entry.split(splitter)
        for (i, sec) in enumerate(sub_split):
            thing_to_add = sec + split_char if i != len(sub_split) - 1 else sec
            new_split.append(thing_to_add)
    return new_split

# will need two pages: one for your first guess, one for subsequent guesses
# actually maybe I could have one page for entering the game and one page for guesses,
# and that page can fork on "have I had a previous guess or not"

# oh: one page for submitting your guess, and one page for seeing whether or not you got
# it right.


@bp.route('/', methods=('GET', 'POST'))
def index():
    if request.method == 'POST':
        user_guess = request.form['user_guess']
        guess_correct = 1 if user_guess == session['episode_name'] else 0
        # add error if somehow you're not yet playing?
        if session['guess_ripe']:
            session['total_guesses'] += 1
            session['correct_guesses'] += guess_correct
        session['guess_ripe'] = False
        return render_template('guess/result.html', user_guess=user_guess)

    else:
        if not 'playing' in session or not session['playing']:
            session['playing'] = True
            session['total_guesses'] = 0
            session['correct_guesses'] = 0
            db = get_db()
            eps = db.execute('SELECT id, title FROM episodes').fetchall()
            names_and_ids = [(ep['title'], ep['id']) for ep in eps]
            names_and_ids.sort(key=lambda x: x[1])
            session['ep_names'] = [ep[0] for ep in names_and_ids]
            session['uuid'] = str(uuid.uuid1())
        random_ep_name = random.choice(session['ep_names'])
        db = get_db()
        contents = db.execute(
            'SELECT contents FROM episodes WHERE title = ?', (random_ep_name,)
        ).fetchone()
        ep_sentence = pick_random_sentence(contents['contents'])
        session['episode_name'] = random_ep_name
        session['sentence'] = ep_sentence
        session['guess_ripe'] = True
        return render_template('guess/index.html')
