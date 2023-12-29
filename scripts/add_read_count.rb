#!/usr/bin/env ruby

# Copyright (c) 2015, Brian C. Thomas
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# 
# The views and conclusions contained in the software and documentation are those
# of the authors and should not be interpreted as representing official policies,
# either expressed or implied, of the FreeBSD Project.

unless ARGV.length >= 1
  $stderr.puts "Need a sam file and a scaffold file - optional third arg is read length (default = 150)"
  exit(1)
end
sam = ARGV[0]
scfile = ARGV[1]
read_length = 150
unless ARGV[2].nil?
  read_length = ARGV[2].to_i
end

ctg2reads = Hash.new

File.open(sam).each do |line|
  next if line =~ /^@/
  line.chomp!
  temp = line.split
  ctg = temp[2]
  if ctg2reads.has_key?(ctg)
    ctg2reads[ctg] += 1
  else
    ctg2reads[ctg] = 1
  end
end
$stderr.puts "done reading sam file"

File.open(scfile).each do |line|
  line.chomp!
  next if line =~ /^\s*$/
  if line =~ /^>(.+)$/
    line = $1
    temp = line.split(/\s+/)
    header_name = temp.shift
    header_description = ""
    if temp.length > 0
      header_description = temp.join(" ")
    end

    out = ">#{header_name}"
    if ctg2reads.has_key?(header_name)
      if header_description.empty?
        out = "#{out} read_length_#{read_length} read_count_#{ctg2reads[header_name]}"
      else
        out = "#{out} #{header_description} read_length_#{read_length} read_count_#{ctg2reads[header_name]}"
      end
    else
      if header_description.empty?
         out = "#{out} read_length_#{read_length} read_count_0"
      else
         out = "#{out} #{header_description} read_length_#{read_length} read_count_0"
      end
    end
    puts out
  else
    puts line
  end
end
