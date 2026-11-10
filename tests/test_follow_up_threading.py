"""A sequence follow-up replies to the email before it, so it threads.

Without In-Reply-To/References, Gmail shows "Re: ..." as a new message, not
a follow-up in the same conversation.
"""

from datetime import datetime, timedelta, timezone

import pytest

from tests.test_outbox_native import (  # noqa: F401  (state is a fixture)
    FakeProvider, make_sender, seed_prospect, state,
)


def _now():
    return datetime.now(timezone.utc).replace(tzinfo=None)


async def _step(state, pid, step, *, provider="", mailbox_id="", campaign="c1"):
    return await state.add_outbox_item(
        prospect_id=pid, to_email="jane@acme.com", subject=f"s{step}",
        body=f"Step {step}. Question?", status="approved", campaign_id=campaign,
        step=step, provider=provider, mailbox_id=mailbox_id,
        send_at=(_now() - timedelta(days=10 - step)).isoformat())


async def _sent(state, item_id, message_id, thread_ref="th-1"):
    await state.update_outbox_item(
        item_id, status="sent", message_id=message_id, thread_ref=thread_ref,
        sent_at=(_now() - timedelta(days=5)).isoformat())


class FakeGmail(FakeProvider):
    name = "gmail"


@pytest.mark.asyncio
async def test_a_follow_up_replies_to_the_email_before_it(state):
    pid = await seed_prospect(state, status="contacted")
    one = await _step(state, pid, 1)
    await _sent(state, one, "<first@example.com>")
    await _step(state, pid, 2)
    provider = FakeProvider()
    await make_sender(state, provider)._drain_due()
    assert [m["subject"] for m in provider.sent] == ["s2"]
    assert provider.sent[0]["in_reply_to"] == "<first@example.com>"
    assert provider.sent[0]["thread_ref"] == ""  # not Gmail: no thread id


@pytest.mark.asyncio
async def test_the_first_email_starts_a_new_thread(state):
    pid = await seed_prospect(state)
    await _step(state, pid, 1)
    provider = FakeProvider()
    await make_sender(state, provider)._drain_due()
    assert provider.sent[0]["in_reply_to"] == ""


@pytest.mark.asyncio
async def test_on_gmail_it_joins_the_thread_the_same_mailbox_started(state):
    pid = await seed_prospect(state, status="contacted")
    one = await _step(state, pid, 1, provider="gmail")
    await _sent(state, one, "<first@example.com>", thread_ref="th-1")
    await _step(state, pid, 2, provider="gmail")
    provider = FakeGmail()
    await make_sender(state, provider)._drain_due()
    assert provider.sent[0]["thread_ref"] == "th-1"
    assert provider.sent[0]["in_reply_to"] == "<first@example.com>"


@pytest.mark.asyncio
async def test_a_gmail_thread_id_from_another_mailbox_is_not_reused(state):
    pid = await seed_prospect(state, status="contacted")
    one = await _step(state, pid, 1, provider="gmail", mailbox_id="other-inbox")
    await _sent(state, one, "<first@example.com>", thread_ref="th-other")
    await _step(state, pid, 2, provider="gmail")
    provider = FakeGmail()
    await make_sender(state, provider)._drain_due()
    assert provider.sent[0]["thread_ref"] == ""
    assert provider.sent[0]["in_reply_to"] == "<first@example.com>"


@pytest.mark.asyncio
async def test_a_provider_id_that_is_not_a_message_id_is_not_sent_as_one(state):
    pid = await seed_prospect(state, status="contacted")
    one = await _step(state, pid, 1)
    await _sent(state, one, "18c0ffee")  # a Gmail API id, not an RFC Message-ID
    await _step(state, pid, 2)
    provider = FakeProvider()
    await make_sender(state, provider)._drain_due()
    assert provider.sent[0]["in_reply_to"] == ""
