# About the Wiki

One of the early goals we set out to accomplish was to develop an intuitive wiki experience catered towards all experience levels and employed cutting edge web design principles. We did not want to just improve on the designs of other wikis; instead, we wanted to build our wiki from the ground up and create something to not only house all of our content for future iGEM teams, but to provide an engaging educational experience. The wiki you see now is the product of months of design, iteration, and dedication; it's something we as the Miami University iGEM team are remarkably proud to call ours.

---

## Mobile-First Design

A core philosophy we had early with the wiki's design is that it needed to be designed to be accessible on as many devices as possible. Consequently, if our wiki looks good on a mobile device, it will translate better to all devices. More importantly than that, with a mobile-first approach, this also becomes a content-first approach. Mobile has the most limitations such as small screen sizes and more; thus, designing within these parameters allows us to prioritize content.

The mobile-first approach organically leads to a design that's more content-focused and user-focused. Users are here for the content. The heart of our site is the content.

## Navigation

You will notice our wiki has a peculiar navigational menu on the left-hand side compared to most wikis. This is not accidental or random. Through user-experience testing, we determined that people were able to more quickly scan and identify menu items with a vertical left-handed navigational menu. As a result of this, users can more quickly navigate between page.

## Reference Tooltips

In a lot of academic papers searching through references can be a tedious chore. One of the key goals we had with our wiki was to streamline the process of not only reading our content but also quickly navigating to any one of our references. To do this, we developed a dynamic tooltip system to quickly see all information on a particular reference and, if applicable, navigate to a reference's website.

For instance, say we wanted to cite the paper _Global food demand and the sustainable intensification of agriculture_ from the Proceedings of the National Academy of Sciences. It's in-text citation will be the following clickable tooltip: <reference identifier="4" />

In addition to the above, all references will be accessible at the bottom a page in the following format:

<div class="box">
  <h3>References</h3>
  <bibliography />
</div>

## Glossary Term Tooltips

Sometimes academic jargon can be hard to understand even when you are familiar with the content. If you are not familiar with the content, it can be even more difficult. Our wiki aims to be more accessible for people of all experience levels by providing simple and easy to use tooltips for frequently used terms.

For instance, the following term is clickable and provides the description without needing to search for it: <span class="note tooltip" title="&lt;i&gt;&lt;b&gt;Example Term&lt;/b&gt;&lt;/i&gt; - This is a description about the example term.">Example Term</span>

---

<div>
  <header class="major">
    <h2>Explore Next</h2>
  </header>
  <p>Now that you know how the wiki works, take time to start exploring all that the Miami University iGEM wiki has to offer!</p>
  <div class="explore-posts">
    <article>
      <a href="/Description" class="image"><img src="assets/images/pic01.jpg" alt="" /></a>
      <h3>Project Description</h3>
      <p>
        The world depends on high agricultural productivity to provide food and resources to local and global
        communities. However, global demand for crop production is expected to increase dramatically. Learn how Miami
        University's CROP could increase the yields of crop plants.
      </p>
      <ul class="actions">
        <li>
          <a href="/Description" class="customButton">More</a>
        </li>
      </ul>
    </article>
    <article>
      <a href="/Team" class="image"
        ><img
          src="assets/images/team/full-team-1.png"
          alt="A photo of the entire Miami University iGEM team wearing Miami University attire."
      /></a>
      <h3>Team</h3>
      <p>
        The work done by Miami University's iGEM team was made possible by a team of dedicate and passionate students
        and advisors from a range of different STEM subject domains! Take a moment to learn more about Miami
        University's committed team!
      </p>
      <ul class="actions">
        <li>
          <a href="/Team" class="customButton">More</a>
        </li>
      </ul>
    </article>
  </div>
</div>
