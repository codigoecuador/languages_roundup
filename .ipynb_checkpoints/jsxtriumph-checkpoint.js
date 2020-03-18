
import React, { Component } from "react";
import { connect } from "react-redux";
import "slick-carousel/slick/slick.css";
import "slick-carousel/slick/slick-theme.css";
import "./Roundup.css";

class RoundupContainer extends Component {
  render() {
    let num;
    this.props.size === "mobile" ? (num = 1) : (num = 2);

    return (
      <div className="main-container">
        <div className="headline roundup-headline">
          <span className="gold">Roundup</span>
        </div>

        <div className="roundup-container-text">
          <div className="subhead center roundup-subhead">
            News Roundup: latest updates on coding and web development
          </div>

          <p><p><b>Skills</b></p>
<p><a href ="https://www.sciencedaily.com/releases/2020/03/200302103735.htm">Not a 'math person'? You may be better at learning to code than you think</a> (3/4/2020) Don't give up on coding if you don't have top-notch math skills, because it has much in common with verbal skills.</p>

<p><a href ="https://www.benzinga.com/money/best-python-course-on-udemy/">Best Python Course on Udemy • Benzinga • Learn Python</a> (2/1/2020) Overview of the best Python courses on Udemy</p>

<p><a href ="https://thenextweb.com/offers/2020/03/14/code-wont-bite-we-promise-in-fact-this-batch-of-courses-could-actually-make-programming-your-friend/">Code won’t bite. We promise. In fact, this batch of courses could actually make programming your friend.</a> (3/14/2020) Overview of the best Python courses on Udemy</p>
<p><b>Scripting/Automation</b></p>
<p><b>Languages</b></p>
<p><a href ="https://www.techrepublic.com/article/why-python-is-likely-to-pass-java-in-popularity/">Why Python is likely to pass Java in popularity</a> (3/10/2020) RedMonk's analysis says that Python has passed Java in popularity, making it the second most popular language. However, the language is unlikely to eclipse Javascript due to the latter's online ubiquity.</p>

<p><a href ="https://www.theregister.co.uk/2020/03/02/redmonk_programming_languages/">If you're writing code in Python, JavaScript, Java and PHP, relax. The hot trendy languages are still miles behind, this survey says</a> (3/2/2020) Python, Java, and Javascript are three of the top languages, and the newer languages such as Go are well behind.</p>

<p><a href ="https://www.infoworld.com/article/3532358/oracle-extends-extended-support-for-java-8.html">Oracle extends Extended support for Java 8</a> (3/16/2020) Not specified</p>

<p><a href ="https://www.infoq.com/news/2020/03/new-relic-jvm-report/">New Relic – the State of Java Report</a> (3/13/2020) Not specified</p>
<p><b>Careers</b></p>
<p><a href ="https://www.infoworld.com/article/3532009/nvidias-rapids-python-analytics-on-the-gpu.html">Nvidia’s Rapids: Python analytics on the GPU</a> (3/11/2020) NVIDIA has created a Rapids project that is intended to help Python developers access their GPUs without knowing complicated low-level code.</p>

<p><a href ="https://www.zdnet.com/article/tesla-know-python-language-and-up-for-a-hardcore-coding-test-get-in-touch/">Know Python language and up for a 'hardcore' coding test? Get in touch, says Tesla</a> (2/4/2020) Elon Musk has said Tesla will hire people who can pass a "hardcore coding test" rather than an educational requirement. This opens the door for skilled but unconventional learners.</p>

<p><a href ="https://www.theguardian.com/world/2020/mar/13/coronavirus-pandemic-visualising-the-global-crisis">The coronavirus pandemic: visualising the global crisis</a> (3/13/2020) A visualization of WHO data regarding the coronavirus. Approximately 4.7 percent of cases required intensive care.</p>

<p><a href ="https://analyticsindiamag.com/why-python-may-lose-its-charm-over-time/">Why Python May Lose Its Charm Over Time?</a> (3/12/2020) Python is a great language, but it has limitations in terms of computational speed. Nothing is perfect, and this article outlines some of its drawbacks.</p>
<p><b>Deep Learning</b></p>
<p><b>Data And Our World</b></p>
</p>
        </div>

      </div>
    );
  }
}

const mapStateToProps = state => {
  return { size: state.size };
};
export default connect(mapStateToProps)(RoundupContainer);