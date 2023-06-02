import pytest

from eigen.nlp import WordCounter


@pytest.fixture
def test_document():
    return """Let me begin by saying thanks to all you who've traveled, from far and wide, to brave the cold today.
We all made this journey for a reason. It's humbling, but in my heart I know you didn't come here just for me, you came here because you believe in what this country can be. In the face of war, you believe there can be peace. In the face of despair, you believe there can be hope. In the face of a politics that's shut you out, that's told you to settle, that's divided us for too long, you believe we can be one people, reaching for what's possible, building that more perfect union.
That's the journey we're on today. But let me tell you how I came to be here. As most of you know, I am not a native of this great state. I moved to Illinois over two decades ago. I was a young man then, just a year out of college; I knew no one in Chicago, was without money or family connections. But a group of churches had offered me a job as a community organizer for $13,000 a year. And I accepted the job, sight unseen, motivated then by a single, simple, powerful idea - that I might play a small part in building a better America.
My work took me to some of Chicago's poorest neighborhoods. I joined with pastors and lay-people to deal with communities that had been ravaged by plant closings. I saw that the problems people faced weren't simply local in nature - that the decision to close a steel mill was made by distant executives; that the lack of textbooks and computers in schools could be traced to the skewed priorities of politicians a thousand miles away; and that when a child turns to violence, there's a hole in his heart no government could ever fill.
It was in these neighborhoods that I received the best education I ever had, and where I learned the true meaning of my Christian faith.
After three years of this work, I went to law school, because I wanted to understand how the law should work for those in need. I became a civil rights lawyer, and taught constitutional law, and after a time, I came to understand that our cherished rights of liberty and equality depend on the active participation of an awakened electorate. It was with these ideas in mind that I arrived in this capital city as a state Senator.
It was here, in Springfield, where I saw all that is America converge - farmers and teachers, businessmen and laborers, all of them with a story to tell, all of them seeking a seat at the table, all of them clamoring to be heard. I made lasting friendships here - friends that I see in the audience today.
It was here we learned to disagree without being disagreeable - that it's possible to compromise so long as you know those principles that can never be compromised; and that so long as we're willing to listen to each other, we can assume the best in people instead of the worst.
That's why we were able to reform a death penalty system that was broken. That's why we were able to give health insurance to children in need. That's why we made the tax system more fair and just for working families, and that's why we passed ethics reforms that the cynics said could never, ever be passed.
It was here, in Springfield, where North, South, East and West come together that I was reminded of the essential decency of the American people - where I came to believe that through this decency, we can build a more hopeful America.
And that is why, in the shadow of the Old State Capitol, where Lincoln once called on a divided house to stand together, where common hopes and common dreams still, I stand before you today to announce my candidacy for President of the United States.
I recognize there is a certain presumptuousness - a certain audacity - to this announcement. I know I haven't spent a lot of time learning the ways of Washington. But I've been there long enough to know that the ways of Washington must change.
The genius of our founders is that they designed a system of government that can be changed. And we should take heart, because we've changed this country before. In the face of tyranny, a band of patriots brought an Empire to its knees. In the face of secession, we unified a nation and set the captives free. In the face of Depression, we put people back to work and lifted millions out of poverty. We welcomed immigrants to our shores, we opened railroads to the west, we landed a man on the moon, and we heard a King's call to let justice roll down like water, and righteousness like a mighty stream.
Each and every time, a new generation has risen up and done what's needed to be done. Today we are called once more - and it is time for our generation to answer that call.
For that is our unyielding faith - that in the face of impossible odds, people who love their country can change it.
That's what Abraham Lincoln understood. He had his doubts. He had his defeats. He had his setbacks. But through his will and his words, he moved a nation and helped free a people. It is because of the millions who rallied to his cause that we are no longer divided, North and South, slave and free. It is because men and women of every race, from every walk of life, continued to march for freedom long after Lincoln was laid to rest, that today we have the chance to face the challenges of this millennium together, as one people - as Americans.
All of us know what those challenges are today - a war with no end, a dependence on oil that threatens our future, schools where too many children aren't learning, and families struggling paycheck to paycheck despite working as hard as they can. We know the challenges. We've heard them. We've talked about them for years.
What's stopped us from meeting these challenges is not the absence of sound policies and sensible plans. What's stopped us is the failure of leadership, the smallness of our politics - the ease with which we're distracted by the petty and trivial, our chronic avoidance of tough decisions, our preference for scoring cheap political points instead of rolling up our sleeves and building a working consensus to tackle big problems.
For the last six years we've been told that our mounting debts don't matter, we've been told that the anxiety Americans feel about rising health care costs and stagnant wages are an illusion, we've been told that climate change is a hoax, and that tough talk and an ill-conceived war can replace diplomacy, and strategy, and foresight. And when all else fails, when Katrina happens, or the death toll in Iraq mounts, we've been told that our crises are somebody else's fault. We're distracted from our real failures, and told to blame the other party, or gay people, or immigrants.
And as people have looked away in disillusionment and frustration, we know what's filled the void. The cynics, and the lobbyists, and the special interests who've turned our government into a game only they can afford to play. They write the checks and you get stuck with the bills, they get the access while you get to write a letter, they think they own this government, but we're here today to take it back. The time for that politics is over. It's time to turn the page.
We've made some progress already. I was proud to help lead the fight in Congress that led to the most sweeping ethics reform since Watergate.
But Washington has a long way to go. And it won't be easy. That's why we'll have to set priorities. We'll have to make hard choices. And although government will play a crucial role in bringing about the changes we need, more money and programs alone will not get us where we need to go. Each of us, in our own lives, will have to accept responsibility - for instilling an ethic of achievement in our children, for adapting to a more competitive economy, for strengthening our communities, and sharing some measure of sacrifice. So let us begin. Let us begin this hard work together. Let us transform this nation.
Let us be the generation that reshapes our economy to compete in the digital age. Let's set high standards for our schools and give them the resources they need to succeed. Let's recruit a new army of teachers, and give them better pay and more support in exchange for more accountability. Let's make college more affordable, and let's invest in scientific research, and let's lay down broadband lines through the heart of inner cities and rural towns all across America.
And as our economy changes, let's be the generation that ensures our nation's workers are sharing in our prosperity. Let's protect the hard-earned benefits their companies have promised. Let's make it possible for hardworking Americans to save for retirement. And let's allow our unions and their organizers to lift up this country's middle-class again.
Let's be the generation that ends poverty in America. Every single person willing to work should be able to get job training that leads to a job, and earn a living wage that can pay the bills, and afford child care so their kids have a safe place to go when they work. Let's do this.
Let's be the generation that finally tackles our health care crisis. We can control costs by focusing on prevention, by providing better treatment to the chronically ill, and using technology to cut the bureaucracy. Let's be the generation that says right here, right now, that we will have universal health care in America by the end of the next president's first term.
Let's be the generation that finally frees America from the tyranny of oil. We can harness homegrown, alternative fuels like ethanol and spur the production of more fuel-efficient cars. We can set up a system for capping greenhouse gases. We can turn this crisis of global warming into a moment of opportunity for innovation, and job creation, and an incentive for businesses that will serve as a model for the world. Let's be the generation that makes future generations proud of what we did here.
Most of all, let's be the generation that never forgets what happened on that September day and confront the terrorists with everything we've got. Politics doesn't have to divide us on this anymore - we can work together to keep our country safe. I've worked with Republican Senator Dick Lugar to pass a law that will secure and destroy some of the world's deadliest, unguarded weapons. We can work together to track terrorists down with a stronger military, we can tighten the net around their finances, and we can improve our intelligence capabilities. But let us also understand that ultimate victory against our enemies will come only by rebuilding our alliances and exporting those ideals that bring hope and opportunity to millions around the globe.
But all of this cannot come to pass until we bring an end to this war in Iraq. Most of you know I opposed this war from the start. I thought it was a tragic mistake. Today we grieve for the families who have lost loved ones, the hearts that have been broken, and the young lives that could have been. America, it's time to start bringing our troops home. It's time to admit that no amount of American lives can resolve the political disagreement that lies at the heart of someone else's civil war. That's why I have a plan that will bring our combat troops home by March of 2008. Letting the Iraqis know that we will not be there forever is our last, best hope to pressure the Sunni and Shia to come to the table and find peace.
Finally, there is one other thing that is not too late to get right about this war - and that is the homecoming of the men and women - our veterans - who have sacrificed the most. Let us honor their valor by providing the care they need and rebuilding the military they love. Let us be the generation that begins this work.
I know there are those who don't believe we can do all these things. I understand the skepticism. After all, every four years, candidates from both parties make similar promises, and I expect this year will be no different. All of us running for president will travel around the country offering ten-point plans and making grand speeches; all of us will trumpet those qualities we believe make us uniquely qualified to lead the country. But too many times, after the election is over, and the confetti is swept away, all those promises fade from memory, and the lobbyists and the special interests move in, and people turn away, disappointed as before, left to struggle on their own.
That is why this campaign can't only be about me. It must be about us - it must be about what we can do together. This campaign must be the occasion, the vehicle, of your hopes, and your dreams. It will take your time, your energy, and your advice - to push us forward when we're doing right, and to let us know when we're not. This campaign has to be about reclaiming the meaning of citizenship, restoring our sense of common purpose, and realizing that few obstacles can withstand the power of millions of voices calling for change.
By ourselves, this change will not happen. Divided, we are bound to fail.
But the life of a tall, gangly, self-made Springfield lawyer tells us that a different future is possible.
He tells us that there is power in words.
He tells us that there is power in conviction.
That beneath all the differences of race and region, faith and station, we are one people.
He tells us that there is power in hope.
As Lincoln organized the forces arrayed against slavery, he was heard to say: "Of strange, discordant, and even hostile elements, we gathered from the four winds, and formed and fought to battle through."
That is our purpose here today.
That's why I'm in this race.
Not just to hold an office, but to gather with you to transform a nation.
I want to win that next battle - for justice and opportunity.
I want to win that next battle - for better schools, and better jobs, and health care for all.
I want us to take up the unfinished business of perfecting our union, and building a better America.
And if you will join me in this improbable quest, if you feel destiny calling, and see as I see, a future of endless possibility stretching before us; if you sense, as I sense, that the time is now to shake off our slumber, and slough off our fear, and make good on the debt we owe past and future generations, then I'm ready to take up the cause, and march with you, and work with you. Together, starting today, let us finish the work that needs to be done, and usher in a new birth of freedom on this Earth."""


@pytest.fixture
def test_sentences():
    sentences = [
        "this is hello world hello hello",
        "and this is goodbye blue sky goodbye",
    ]
    return sentences


@pytest.fixture
def test_preprocess_sentences():
    sentences = [
        "Let me begin by saying thanks to all you who've traveled, from far and wide, to brave the cold today."
    ]
    return sentences


@pytest.fixture
def test_counter(test_sentences):
    counter = WordCounter()
    for i, s in enumerate(test_sentences):
        words = s.split(" ")
        counter.update(words, "test_document", i)
    return counter, test_sentences
