import functools
import random

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from guess_that_axrp.db import get_db

bp = Blueprint('guess', __name__)


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
    return random.choice(sep_bang)


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


@bp.route('/')
def index():
    db = get_db()
    eps = db.execute('SELECT title, contents FROM episodes').fetchall()
    random_ep = random.choice(eps)
    ep_name = random_ep[0]
    ep_sentence = pick_random_sentence(random_ep[1])
    all_titles = list(map(lambda tc_tup: tc_tup[0], eps))
    # hmmm, it's dangerous to send the user the episode name in the html/javascript.
    # maybe I can add it to g?
    g.next_episode_name = ep_name
    # also need to have a list of all the titles to select from
    return render_template(
        'guess/index.html', ep_sentence=ep_sentence, all_titles=all_titles,
    )
